import toml
from importlib.resources import files

def getConfig(config, key):
    try:
        return config[key]
    except KeyError:
        print(f'WARNING! empty key \'{key}\' in config: {config}')
        return None

def mergeConfig(a: dict, b: dict, path=[]):
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                mergeConfig(a[key], b[key], path + [str(key)])
            elif a[key] != b[key]:
                if isinstance(a[key], list) and isinstance(b[key], list):
                    a[key] += b[key]
                else: 
                    raise Exception('Conflict at ' + '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

def includeTomls(config, includes):
    result = config
    del result['project']['includes']

    for include in includes:
        include_config = toml.loads(files('pooUp.resources').joinpath(include + '.toml').read_text())
        result = mergeConfig(result, include_config)

    new_includes = getConfig(getConfig(result, 'project'), 'includes')
    if new_includes:
        result = includeTomls(result, new_includes)

    return result
