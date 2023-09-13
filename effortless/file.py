import os
from importlib.resources import files
from .define import Define
from .config import getConfig, resolveOrigin

class File:
    def __init__(self, file):
        self.folder = Define.defineIn(getConfig(file, 'folder'))
        self.name = Define.defineIn(getConfig(file, 'name'))
        self.origin = Define.defineIn(getConfig(file, 'origin', True))
        self.create = getConfig(file, 'create', True)
        self.content = Define.defineIn(getConfig(file, 'content', True))
        self.is_bytes = getConfig(file, 'is_bytes', True)

    def fromFiles(files):
        objs = []

        if files:
            for file in files:
                objs.append(File(file))

        return objs

    def generate(self, project):
        if not self.folder:
            self.folder = ''
        if not self.content:
            self.content = ''
        if self.is_bytes == None:
            self.is_bytes = True

        path = project.project_dir + self.folder + '/'

        os.makedirs(path, exist_ok = True)

        path += self.name

        self.origin_path = resolveOrigin(self.origin)

        with open(path, 'w' + ('b' if self.is_bytes and not self.create else '')) as f:
            if self.create:
                f.write(self.content)
            elif self.origin.startswith('$') and self.is_bytes:
                f.write(files('effortless.resources').joinpath(self.origin_path).joinpath(self.name).read_bytes())
            elif self.origin.startswith('$') and not self.is_bytes:
                f.write(Define.defineIn(files('effortless.resources').joinpath(self.origin_path).joinpath(self.name).read_text()))
            elif self.is_bytes:
                with open(self.origin, 'rb') as o:
                    f.write(o.read())
            elif not self.is_bytes:
                with open(self.origin, 'r') as o:
                    f.write(Define.defineIn(o.read()))
