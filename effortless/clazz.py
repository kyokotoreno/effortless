from importlib.resources import files
from .field import Field
from .method import Method
from .define import Define
from .config import getConfig, resolveOrigin

class Clazz:
    template = """package {package};
{inports}public class {name}{extends}{implements} {{
{fields}{methods}}}
"""
    import_template = "import {inport};\n"

    def __init__(self, clazz):
        self.package = getConfig(clazz, 'package')
        self.imports = getConfig(clazz, 'imports', True)
        self.name = getConfig(clazz, 'name')
        self.extends = getConfig(clazz, 'extends', True)
        self.implements = getConfig(clazz, 'implements', True)
        self.fields = Field.fromFields(getConfig(clazz, 'fields', True))
        self.methods = Method.fromMethods(getConfig(clazz, 'methods', True))
        self.origin = getConfig(clazz, 'origin', True)

    def fromClasses(classes):
        objs = []

        if classes:
            for clazz in classes:
                objs.append(Clazz(clazz))

        return objs

    def genImports(self):
        self.gen_imports = ''

        if self.imports:
            for inport in self.imports:
                self.gen_imports += self.import_template.format(inport=inport)

    def genExtends(self):
        self.gen_extends = ''

        if self.extends:
            self.gen_extends = ' extends ' + self.extends

    def genImplements(self):
        self.gen_implements = ''

        if self.implements:
            self.gen_implements = ' implements ' + ','.join(self.implements)

    def genFields(self, t):
        self.gen_fields = ''

        if self.fields:
            for field in self.fields:
                self.gen_fields += field.generate(t)

    def genMethods(self, t):
        self.gen_methods = ''

        if self.methods:
            for method in self.methods:
                self.gen_methods += method.generate(t)

    def generate(self, project, t):
        if not self.origin:
            self.origin = ''

        filename = self.name + '.java'
        path = project.src_dir + self.package.replace('.', '/') + '/' + filename

        with open(path, 'w') as f:
            self.gen = ''

            if self.origin.startswith('$'):
                self.gen = files('effortless.resources').joinpath(resolveOrigin(self.origin)).joinpath(filename).read_text()
            elif self.origin:
                with open(self.origin, 'r') as o:
                    self.gen = o.read()
            else:
                self.genImports()
                self.genExtends()
                self.genImplements()
                self.genFields(t)
                self.genMethods(t)

                self.gen = self.template.format(
                    package=self.package,
                    inports=self.gen_imports,
                    name=self.name,
                    fields=self.gen_fields,
                    methods=self.gen_methods,
                    extends=self.gen_extends,
                    implements=self.gen_implements
                )

            f.write(Define.defineIn(self.gen))
