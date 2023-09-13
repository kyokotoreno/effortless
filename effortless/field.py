from .config import getConfig

class Field:
    template = """{t}{accessor} {type} {name}{init};
"""

    def __init__(self, field):
        self.accessor = getConfig(field, 'accessor')
        self.type = getConfig(field, 'type')
        self.name = getConfig(field, 'name')
        self.init = getConfig(field, 'init', True)

    def fromFields(fields):
        objs = []

        if fields:
            for field in fields:
                objs.append(Field(field))

        return objs

    def generate(self, t):
        self.gen_init = ''

        if self.init:
            self.gen_init = ' = ' + self.init

        return self.template.format(t=t, accessor=self.accessor, type=self.type, name=self.name, init=self.gen_init)