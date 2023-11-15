"""
CustomHandler for Daos & Entidades, Luz Helena

params:

    - name: str
    - entity_imports: list (str)
    - dao_imports: list (str)
    - fields: dict [accessor: str, type: str, name: str]
    - primary_key: str
    - table: str

"""

from effortless.config import getConfig
from effortless.define import Define
from effortless.clazz import Clazz
from effortless.field import Field
from effortless.argument import Argument
from effortless.method import Method

from inflection import camelize, underscore
from itertools import chain
from copy import deepcopy

class CustomHandler:
    dao_methods = {
        'register': {
            'accessor': 'public',
            'return_type': 'Boolean',
            'name': 'registrar',
            'annotations': ['Override'],
            'arguments': [{'type': '%entity_name%', 'name': 'elObjeto'}],
            'body': '''cadenaSql = "INSERT INTO %table_name% (%entity_fields%) VALUES (%values%)";

try {
    consulta = conexion.prepareStatement(cadenaSql);

%consulta_sets%

    cantidad = consulta.executeUpdate();

    conexion.close();
    return cantidad > 0;
} catch (SQLException ex) {
    Logger.getLogger(%dao_name%.class.getName()).log(Level.SEVERE, null, ex);
    return false;
}'''
        },
        'consult': {
            'accessor': 'public',
            'return_type': 'List<%entity_name%>',
            'name': 'consultar',
            'annotations': ['Override'],
            'arguments': [{'type': 'String', 'name': 'orden'}],
            'body': '''if (orden.isEmpty()) {
    orden = "%primary_key%";
}

cadenaSql = "SELECT %entity_fields% FROM %table_name% ORDER BY " + orden;

try {
    consulta = conexion.prepareStatement(cadenaSql);

    registros = consulta.executeQuery();
    cantidad = registros.getFetchSize();

    ArrayList<%entity_name%> %table_name% = new ArrayList<%entity_name%>();

    while (registros.next()) {
        %entity_name% %entity_name_lower% = new %entity_name%();

%consulta_gets%

        %table_name%.add(%entity_name_lower%);
    }

    conexion.close();
    return %table_name%;
} catch (SQLException ex) {
    Logger.getLogger(%dao_name%.class.getName()).log(Level.SEVERE, null, ex);
    return null;
}'''
        },
        'search': {
            'accessor': 'public',
            'return_type': '%entity_name%',
            'name': 'buscar',
            'annotations': ['Override'],
            'arguments': [{'type': 'Integer', 'name': 'llavePrimaria'}],
            'body': '''cadenaSql = "SELECT %entity_fields% FROM %table_name% WHERE %primary_key% = ?";

try {
    consulta = conexion.prepareStatement(cadenaSql);
    consulta.setInt(1, llavePrimaria);

    registros = consulta.executeQuery();
    cantidad = registros.getFetchSize();

    registros.next();

    %entity_name% %entity_name_lower% = new %entity_name%();

%consulta_gets%

    conexion.close();
    return %entity_name_lower%;
} catch (SQLException ex) {
    Logger.getLogger(%dao_name%.class.getName()).log(Level.SEVERE, null, ex);
    return null;
}'''
        },
        'delete': {
            'accessor': 'public',
            'return_type': 'Boolean',
            'name': 'eliminar',
            'annotations': ['Override'],
            'arguments': [{'type': 'Integer', 'name': 'llavePrimaria'}],
            'body': '''cadenaSql = "DELETE FROM %table_name% WHERE %primary_key% = ?";

try {
    consulta = conexion.prepareStatement(cadenaSql);
    consulta.setInt(1, llavePrimaria);

    cantidad = consulta.executeUpdate();

    conexion.close();
    return cantidad > 0;
} catch (SQLException ex) {
    Logger.getLogger(%dao_name%.class.getName()).log(Level.SEVERE, null, ex);
    return false;
}''',
        },
        'update': {
            'accessor': 'public',
            'return_type': 'Boolean',
            'name': 'actualizar',
            'annotations': ['Override'],
            'arguments': [{'type': '%entity_name%', 'name': 'elObjeto'}],
            'body': '''cadenaSql = "UPDATE %table_name% SET %entity_set_fields% WHERE %primary_key% = ?";

try {
    consulta = conexion.prepareStatement(cadenaSql);

%consulta_sets%

    cantidad = consulta.executeUpdate();

    conexion.close();
    return cantidad > 0;
} catch (SQLException ex) {
    Logger.getLogger(%dao_name%.class.getName()).log(Level.SEVERE, null, ex);
    return false;
}'''
        },
        'total': {
            'accessor': 'public',
            'return_type': 'Integer',
            'name': 'totalRegistros',
            'annotations': ['Override'],
            'body': '''cadenaSql = "SELECT COUNT(%primary_key%) FROM %table_name%";

try {
    consulta = conexion.prepareStatement(cadenaSql);
    registros = consulta.executeQuery();
    
    registros.next();
    cantidad = registros.getInt(1);

    conexion.close();
    return cantidad;
} catch (SQLException ex) {
    Logger.getLogger(%dao_name%.class.getName()).log(Level.SEVERE, null, ex);
    return null;
}'''
        },
    }

    def __init__(self, custom):
        self.name = getConfig(custom, 'name')
        self.entity_imports = getConfig(custom, 'entity_imports', True)
        self.dao_imports = getConfig(custom, 'dao_imports', True)
        self.fields = Field.fromFields(getConfig(custom, 'fields'))
        self.primary_key = getConfig(custom, 'primary_key')
        self.table = getConfig(custom, 'table')

    def fromToHandle(to_handle):
        objs = []
        
        if to_handle:
            for handle in to_handle:
                objs.append(CustomHandler(handle))

        return objs

    def genGettersSetters(self, fields: list[Field]):
        self.gen_getters = []
        self.gen_setters = []

        for field in fields:
            getterMethod = Method({})
            getterMethod.accessor = 'public' if field.accessor == 'private' or field.accessor == 'public' else 'protected'
            getterMethod.return_type = field.type
            getterMethod.name = camelize('get_' + underscore(field.name), False)
            getterMethod.body = f"return this.{field.name};"

            setterMethod = Method({})
            setterMethod.accessor = getterMethod.accessor
            setterMethod.arguments = Argument.fromArguments([{'type': field.type, 'name': field.name}])
            setterMethod.name = camelize('set_' + underscore(field.name), False)
            setterMethod.body = f'this.{field.name} = {field.name};'

            self.gen_getters.append(getterMethod)
            self.gen_setters.append(setterMethod)

    def mapTypeToRegistryType(self, type):
        map = {
            'Integer': 'Int',
            'String': 'String',
            'Short': 'Short'
        }
		
        try:
            return map[type.removesuffix(' ')]
        except KeyError:
            return None

    def genDaoMethodRegister(self, daoClazz):
        setter_i = 1
        gen_daosetters = ''
        for getter in list(filter(lambda x : not x.name.startswith(camelize('get_' + self.primary_key, False)), self.gen_getters)):
            type = self.mapTypeToRegistryType(getter.return_type)
            if not type:
                gen_daosetters += f'    // Custom Type {getter.return_type.removesuffix(" ")}, please program manually\n'
                print(f'WARNING!: Custom Type {getter.return_type.removesuffix(" ")}, please program manually in method register dao \'{self.name}\'')
            else:
                gen_daosetters += f'    consulta.set{type}({setter_i}, elObjeto.{getter.name}());\n'
            setter_i += 1

        mfields = [*filter(lambda x : not x.name.startswith(self.primary_key), self.fields)]

        defines = {
            'values': ', '.join(['?'] * len(mfields)),
            'entity_fields': ', '.join(map(lambda x : x.name, mfields)),
            'entity_name': self.name,
            'entity_name_lower': self.name.lower(),
            'table_name': self.table,
            'dao_name': 'Dao' + self.name,
            'consulta_sets': gen_daosetters
        }

        methodRegister = Method(self.dao_methods['register'])

        for argument in methodRegister.arguments:
            argument.type = Define.defineWith(argument.type, defines)

        methodRegister.body = Define.defineWith(methodRegister.body, defines)

        daoClazz.methods.append(methodRegister)

    def genDaoMethodConsult(self, daoClazz):
        getter_i = 1
        gen_daogetters = ''
        for getter in self.gen_getters:
            type = self.mapTypeToRegistryType(getter.return_type)
            if not type:
                gen_daogetters += f'        // Custom Type {getter.return_type.removesuffix(" ")}, please program manually\n'
                print(f'WARNING!: Custom Type {getter.return_type.removesuffix(" ")}, please program manually in method consult dao \'{self.name}\'')
            else:
                gen_daogetters += f'        {self.name.lower()}.{getter.name.replace("get", "set")}(registros.get{type}({getter_i}));\n'
            getter_i += 1

        defines = {
            'entity_fields': ', '.join(map(lambda x : x.name, self.fields)),
            'entity_name': self.name,
            'entity_name_lower': self.name.lower(),
            'table_name': self.table,
            'primary_key': self.primary_key,
            'dao_name': 'Dao' + self.name,
            'consulta_gets': gen_daogetters
        }

        methodConsult = Method(self.dao_methods['consult'])

        methodConsult.return_type = Define.defineWith(methodConsult.return_type, defines)
        methodConsult.body = Define.defineWith(methodConsult.body, defines)

        daoClazz.methods.append(methodConsult)

    def genDaoMethodSearch(self, daoClazz):
        getter_i = 1
        gen_daogetters = ''

        for getter in self.gen_getters:
            type = self.mapTypeToRegistryType(getter.return_type)
            if not type:
                gen_daogetters += f'     // Custom Type {getter.return_type.removesuffix(" ")}, please program manually\n'
                print(f'WARNING!: Custom Type {getter.return_type.removesuffix(" ")}, please program manually in method search dao \'{self.name}\'')
            else:
                gen_daogetters += f'    {self.name.lower()}.{getter.name.replace("get", "set")}(registros.get{type}({getter_i}));\n'
            getter_i += 1

        defines = {
            'entity_fields': ', '.join(map(lambda x : x.name, self.fields)),
            'entity_name': self.name,
            'entity_name_lower': self.name.lower(),
            'table_name': self.table,
            'primary_key': self.primary_key,
            'dao_name': 'Dao' + self.name,
            'consulta_gets': gen_daogetters
        }

        methodSearch = Method(self.dao_methods['search'])

        methodSearch.return_type = Define.defineWith(methodSearch.return_type, defines)
        methodSearch.body = Define.defineWith(methodSearch.body, defines)

        daoClazz.methods.append(methodSearch)

    def genDaoMethodDelete(self, daoClazz):
        defines = {
            'table_name': self.table,
            'primary_key': self.primary_key,
            'dao_name': 'Dao' + self.name
        }

        methodDelete = Method(self.dao_methods['delete'])

        methodDelete.body = Define.defineWith(methodDelete.body, defines)

        daoClazz.methods.append(methodDelete)

    def genDaoMethodUpdate(self, daoClazz):
        setter_i = 1
        gen_daosetters = ''
        for getter in list(filter(lambda x : not x.name.startswith(camelize('get_' + self.primary_key, False)), self.gen_getters)):
            type = self.mapTypeToRegistryType(getter.return_type)
            if not type:
                gen_daosetters += f'    // Custom Type {getter.return_type.removesuffix(" ")}, please program manually\n'
                print(f'WARNING!: Custom Type {getter.return_type.removesuffix(" ")}, please program manually in method register dao \'{self.name}\'')
            else:
                gen_daosetters += f'    consulta.set{type}({setter_i}, elObjeto.{getter.name}());\n'
            setter_i += 1

        mfields = [*filter(lambda x : not x.name.startswith(self.primary_key), self.fields)]

        methodUpdate = Method(self.dao_methods['update'])

        defines = {
            'entity_name': self.name,
            'table_name': self.table,
            'primary_key': self.primary_key,
            'dao_name': 'Dao' + self.name,
            'entity_set_fields': ', '.join(map(lambda x: x.name + ' = ?', mfields)),
            'consulta_sets': gen_daosetters
        }

        for argument in methodUpdate.arguments:
            argument.type = Define.defineWith(argument.type, defines)

        methodUpdate.body = Define.defineWith(methodUpdate.body, defines)

        daoClazz.methods.append(methodUpdate)

    def genDaoMethodTotal(self, daoClazz):
        defines = {
            'table_name': self.table,
            'primary_key': self.primary_key,
            'dao_name': 'Dao' + self.name
        }

        methodTotal = Method(self.dao_methods['total'])

        methodTotal.body = Define.defineWith(methodTotal.body, defines)

        daoClazz.methods.append(methodTotal)

    def genDaoClazz(self, project):
        if not self.dao_imports:
            self.dao_imports = []

        daoClazz = Clazz({})

        daoClazz.package = 'edu.usta.daos'
        defaultDaoImports = [
            'edu.usta.configuracion.MiConexion', 
            'edu.usta.interfaces.Funcionalidad',
            'java.sql.SQLException',
            'java.util.ArrayList',
            'java.util.List',
            'java.util.logging.Level',
            'java.util.logging.Logger',
            'edu.usta.entidades.' + self.name
        ]
        daoClazz.imports = defaultDaoImports + self.dao_imports
        daoClazz.name = 'Dao' + self.name
        daoClazz.extends = 'MiConexion'
        daoClazz.implements = ['Funcionalidad<' + self.name + '>']
        daoClazz.methods = []

        self.genDaoMethodRegister(daoClazz)
        self.genDaoMethodConsult(daoClazz)
        self.genDaoMethodSearch(daoClazz)
        self.genDaoMethodDelete(daoClazz)
        self.genDaoMethodUpdate(daoClazz)
        self.genDaoMethodTotal(daoClazz)

        daoClazz.generate(project, ' ' * 4)

    def genEntityClazz(self, project):
        entityClazz = Clazz({})

        entityClazz.package = 'edu.usta.entidades'
        entityClazz.imports = self.entity_imports
        entityClazz.name = self.name

        self.camel_fields = []

        for field in deepcopy(self.fields):
            field.name = camelize(field.name, False)
            self.camel_fields.append(field)

        entityClazz.fields = self.camel_fields
        self.genGettersSetters(self.camel_fields)

        entityEmptyConstructor = Method({})
        entityEmptyConstructor.is_constructor = True
        entityEmptyConstructor.accessor = 'public'
        entityEmptyConstructor.name = self.name
        entityEmptyConstructor.body = ''

        entityConstructor = Method({})
        entityConstructor.is_constructor = True
        entityConstructor.accessor = 'public'
        entityConstructor.name = self.name
        mfields = [*filter(lambda x : not x.name.startswith(self.primary_key), self.fields)]

        constSetters = []
        entityConstructor.arguments = []

        for mfield in mfields:
            constSetters.append(f'this.{camelize(mfield.name, False)} = {camelize(mfield.name, False)};')
            entityConstructor.arguments += Argument.fromArguments([{'type': mfield.type, 'name': camelize(mfield.name, False)}])

        entityConstructor.body = '\n'.join(constSetters)

        entityClazz.methods = [entityEmptyConstructor, entityConstructor] + [*chain(*zip(self.gen_getters, self.gen_setters))]

        entityClazz.generate(project, ' ' * 4)

    def generate(self, project):
        self.genEntityClazz(project)
        self.genDaoClazz(project)
        pass
