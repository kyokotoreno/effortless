import re
from .config import getConfig

class Define:
    defines = []
    
    def fromDefines(defines):
        if not defines == None:
            Define.defines = defines

    def get(name):
        return Define.defines[name]

    def defineIn(string):
        if string == None:
            return None

        newstring = ''
        start = 0

        for m in re.finditer(r"%(\w+)%", string):
            end, newstart = m.span()
            newstring += string[start:end]
            name = m.group(1)
            rep = Define.get(name)
            newstring += rep
            start = newstart

        newstring += string[start:]

        return newstring
