from importlib import import_module
from .config import getConfig

class CustomHandler:
    def __init__(self, customHandler):
        self.name = getConfig(customHandler, 'name')
        self.array = getConfig(customHandler, 'array')
        self.handler = getConfig(customHandler, 'handler')

        print('CUSTOM HANDLER LOADED! \'' + self.name + '\'')

    def fromCustomHandlers(custom_handlers):
        if not custom_handlers:
            return

        objs = []

        for custom in custom_handlers:
            objs.append(CustomHandler(custom))

        return objs

    def generate(self, project):
        if not self.handler.startswith('.'):
            self.handler = '.' + self.handler

        custom_module = import_module(self.handler, 'effortless.resources.custom_handlers')
        CustomHandlerClazz = getattr(custom_module, 'CustomHandler')

        custom_handles = CustomHandlerClazz.fromToHandle(self.to_handle)

        for custom_handle in custom_handles:
            custom_handle.generate(project)
