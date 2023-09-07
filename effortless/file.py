import os
from importlib.resources import files
from .define import Define
from .config import getConfig

class File:
    def __init__(self, file):
        self.folder = Define.defineIn(getConfig(file, 'folder'))
        self.name = Define.defineIn(getConfig(file, 'name'))
        self.origin = Define.defineIn(getConfig(file, 'origin'))
        self.create = getConfig(file, 'create')

    def fromFiles(files):
        objs = []

        if not files == None:
            for file in files:
                objs.append(File(file))

        return objs

    def generate(self, project):
        path = project.project_dir + self.folder + '/'

        os.makedirs(path, exist_ok=True)

        path += self.name

        with open(path, 'wb') as f:
            if self.create:
                f.write(b'')
            elif self.origin == '$':
                f.write(files('effortless.resources').joinpath(self.name).read_bytes())
            else:
                with open(self.origin, 'rb') as o:
                    f.write(o.read())
