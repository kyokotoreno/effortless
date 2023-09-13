from .config import getConfig

class Argument:
    template = "{type} {name}{init}"

    def __init__(self, argument):
        self.type = getConfig(argument, 'type')
        self.name = getConfig(argument, 'name')
        self.init = getConfig(argument, 'init', True)

    def fromArguments(arguments):
        objs = []

        if arguments:
            for argument in arguments:
                objs.append(Argument(argument))

        return objs

    def generate(self):
        self.gen_init = ''

        if self.init:
            self.gen_init = ' = ' + self.init

        return self.template.format(type=self.type, name=self.name, init=self.gen_init)