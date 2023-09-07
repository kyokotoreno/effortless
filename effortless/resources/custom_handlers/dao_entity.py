"""
CustomHandler for DaoEntity

params:

    - name: str
    - imports: list (str)
    - fields: dict [accessor: str, type: str, name: str]
"""

from effortless.config import getConfig
from effortless.clazz import Clazz
from effortless.field import Field

class CustomHandler:
    def __init__(self, custom):
        self.name = getConfig(custom, 'name')
        self.imports = getConfig(custom, 'imports')
        self.fields = Field.fromFields(getConfig(custom, 'fields'))

    def fromToHandle(to_handle):
        objs = []
        
        for handle in to_handle:
            objs.append(CustomHandler(handle))

        return objs

    def genGetterSetter(self, field: Field):
        getter = {
            'name': f'get{field.field}'
        }

    def generate(self, project):
        self.genClazz = Clazz({})
        pass
