import toml
import os
from .define import Define
from .custom_handler import CustomHandler
from .clazz import Clazz
from .file import File
from .config import getConfig, includeTomls

class Project:
    def __init__(self, toml_path, path='out', src_path='src'):
        if not path.endswith('/'):
            path += '/'

        self.config = toml.load(toml_path)
        self.project = self.config['project']

        if not self.project:
            raise RuntimeError('\'project\' key not defined')

        self.project_dir = path + getConfig(self.project, 'name') + '/'
        self.src_dir = self.project_dir + src_path + '/'

        self.config = includeTomls(self.config, getConfig(self.project, 'includes'))
        self.project = self.config['project'] # update project

        Define.fromDefines(getConfig(self.config, 'defines'))

        self.packages = getConfig(self.project, 'packages')
        self.custom_handlers = CustomHandler.fromCustomHandlers(getConfig(self.project, 'custom_handlers'))
        self.classes = Clazz.fromClasses(getConfig(self.config, 'classes'))
        self.files = File.fromFiles(getConfig(self.config, 'files'))

    def genPackages(self):
        for package in self.packages:
            path = self.src_dir + (Define.defineIn(package)).replace('.', '/')
            os.makedirs(path, exist_ok=True)

    def genCustomHandlers(self):
        for custom in self.custom_handlers:
            to_handle = getConfig(self.config, custom.array) # get custom array of elements to handle
            custom.to_handle = to_handle # inject custom array of elements to handle
            custom.generate(self) # generate

    def genClasses(self):
        for clazz in self.classes:
            clazz.generate(self, ' ' * 4)

    def genFiles(self):
        for file in self.files:
            file.generate(self)

    def generate(self):
        self.genPackages()
        self.genCustomHandlers()
        self.genClasses()
        self.genFiles()
