from .config import getConfig

class Field:
    template = """{t}{accessor} {type} {name}{init};
"""

    def __init__(self, field):
        self.accessor = getConfig(field, 'accessor')
        self.type = getConfig(field, 'type')
        self.name = getConfig(field, 'name')
        self.init = getConfig(field, 'init')

    def fromFields(fields):
        objFields = []

        if not fields == None:
            for field in fields:
                objFields.append(Field(field))

        return objFields

    def generate(self, t):
        if self.init:
            init = ' = ' + self.init

        return self.template.format(t=t, accessor=self.accessor, type=self.type, name=self.name, init=init)