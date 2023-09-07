from importlib.resources import files
from .field import Field
from .method import Method
from .define import Define
from .config import getConfig

class Clazz:
    template = """package {package};
{inports}public class {name}{extends}{implements} {{
    {fields}{methods}}}
"""
    import_template = "import {inport};\n"

    def __init__(self, clazz):
        self.package = getConfig(clazz, 'package')
        self.imports = getConfig(clazz, 'imports')
        self.name = getConfig(clazz, 'name')
        self.extends = getConfig(clazz, 'extends')
        self.implements = getConfig(clazz, 'implements')
        self.fields = Field.fromFields(getConfig(clazz, 'fields'))
        self.methods = Method.fromMethods(getConfig(clazz, 'methods'))
        self.origin = getConfig(clazz, 'origin')

    def fromClasses(classes):
        if not classes:
            return

        objs = []

        for clazz in classes:
            objs.append(Clazz(clazz))

        return objs

    def genImports(self):
        if self.imports:
            for inport in self.imports:
                self.gen_imports += self.import_template.format(inport)

    def genExtends(self):
        if self.extends:
            self.gen_extends = ' extends ' + self.extends

    def genImplements(self):
        if self.implements:
            self.gen_implements = ' implements ' + self.implements.join(',')

    def genFields(self, t):
        if self.fields:
            for field in self.fields:
                self.gen_fields += field.generate(t)

    def genMethods(self, t):
        if self.methods:
            for method in self.methods:
                self.gen_methods += method.generate(t)

    def generate(self, project, t):
        filename = self.name + '.java'
        path = project.src_dir + self.package.replace('.', '/') + '/' + filename

        with open(path, 'w') as f:
            self.gen = ''

            if self.origin == '$':
                self.gen = files('effortless.resources').joinpath(filename).read_text()
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
