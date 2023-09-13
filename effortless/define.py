import re
from .config import getConfig

class Define:
    regex = r'%(\w+)%'
    defines = []
    
    def fromDefines(defines):
        if defines:
            Define.defines = defines

    def add(name, value):
        Define.defines[name] = value

    def get(name):
        try:
            return Define.defines[name]
        except KeyError:
            print('WARNING DEFINE NOT FOUND! \'' + name + '\'')
            return ''
    
    def getCustomOrFallback(name, custom_defines):
        try:
            return custom_defines[name]
        except KeyError:
            print('WARNING CUSTOM DEFINE FALLBACK! \'' + name + '\'')
            return Define.get(name)

    def defineIn(string):
        if not string:
            return None

        newstring = ''
        start = 0

        for m in re.finditer(Define.regex, string):
            end, newstart = m.span()
            newstring += string[start:end]
            name = m.group(1)
            rep = Define.get(name)
            newstring += rep
            start = newstart

        newstring += string[start:]

        return newstring

    def defineWith(string, custom_defines):
        if not string:
            return None

        newstring = ''
        start = 0

        for m in re.finditer(Define.regex, string):
            end, newstart = m.span()
            newstring += string[start:end]
            name = m.group(1)
            rep = Define.getCustomOrFallback(name, custom_defines)
            newstring += rep
            start = newstart

        newstring += string[start:]

        return newstring
