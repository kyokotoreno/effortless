"""
CustomHandler for DaoEntity

params:

    - name: str
    - entity_imports: list (str)
    - dao_imports: list (str)
    - fields: dict [accessor: str, type: str, name: str]
"""

from effortless.config import getConfig
from effortless.clazz import Clazz
from effortless.field import Field
from effortless.argument import Argument
from effortless.method import Method

class CustomHandler:
    def __init__(self, custom):
        self.name = getConfig(custom, 'name')
        self.entity_imports = getConfig(custom, 'entity_imports')
        self.dao_imports = getConfig(custom, 'dao_imports')
        self.fields = Field.fromFields(getConfig(custom, 'fields'))

    def fromToHandle(to_handle):
        objs = []
        
        if to_handle:
            for handle in to_handle:
                objs.append(CustomHandler(handle))

        return objs

    def camelCase(self, s):
        # saving first and rest using split()
        init, *temp = s.split('_')
        
        # using map() to get all words other than 1st
        # and titlecasing them
        res = ''.join([init.lower(), *map(str.title, temp)])
        return res

    def genGettersSetters(self, fields: list[Field]):
        self.gen_getters_setters = []

        for field in fields:
            getterMethod = Method({})
            getterMethod.accessor = 'public' if field.accessor == 'private' or field.accessor == 'public' else 'protected'
            getterMethod.return_type = field.type
            getterMethod.name = self.camelCase('get_' + field.name)
            getterMethod.body = f"return this.{field.name};"

            setterMethod = Method({})
            setterMethod.accessor = getterMethod.accessor
            setterMethod.arguments = Argument.fromArguments([{'type': field.type, 'name': field.name}])
            setterMethod.name = self.camelCase('set_' + field.name)
            setterMethod.body = f"this.{field.name} = {field.name};"

            self.gen_getters_setters.append(getterMethod)
            self.gen_getters_setters.append(setterMethod)

    def genDaoClazz(self):
        pass

    def genEntityClazz(self, project):
        entityClazz = Clazz({})

        entityClazz.package = 'edu.usta.entidades'
        entityClazz.imports = self.entity_imports
        entityClazz.name = self.name
        entityClazz.fields = self.fields
        self.genGettersSetters(self.fields)
        entityClazz.methods = self.gen_getters_setters

        entityClazz.generate(project, ' ' * 4)

    def generate(self, project):
        self.genEntityClazz(project)
        pass
