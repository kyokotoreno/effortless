import toml
from importlib.resources import files

def getConfig(config, key, optional = False):
    try:
        return config[key]
    except KeyError:
        if not optional and config:
            raise RuntimeWarning(f'WARNING! non optional empty key \'{key}\' in non empty config: {config}')
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
                    a[key] = b[key]
                    print('WARNING INCLUDE OVERRIDE! Conflict at ' + '.'.join(path + [str(key)]) + ', solved with value: ' + a[key])
        else:
            a[key] = b[key]
    return a

def includeTomls(config, includes):
    result = config
    del result['project']['includes']

    for include in includes:
        include_config = toml.loads(files('effortless.resources').joinpath(include + '.toml').read_text())
        result = mergeConfig(dict(include_config), result)

    new_includes = getConfig(getConfig(result, 'project', True), 'includes', True)
    if new_includes:
        result = includeTomls(result, new_includes)

    return result

def resolveOrigin(origin):
    path = str(origin)

    if path.startswith('$'):
        path = path.removeprefix('$')

    return path
