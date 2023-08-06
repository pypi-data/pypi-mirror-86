from collections.abc import Iterable

def get_deep_attr(o, path, **kwargs):
    if path == '':
        return o
    sub_path = path.split('/', 2)
    
    attr_name = sub_path.pop(0)
    if isinstance(o, Iterable) and (attr_name in o):
        result = o[attr_name]
    elif hasattr(o, attr_name):
        result = getattr(o, attr_name)
    else:
        if 'default' in kwargs:
            result = kwargs['default']
        else:
            raise KeyError(f'Path {path} not found')
    
    if sub_path:
        result = get_deep_attr(result, sub_path[0], **kwargs)

    return result

def get_deep_attr_getter(path, **kwargs):
    return lambda o: get_deep_attr(o, path, **kwargs)


def map_rows(o, map, root=''):
    item_list = get_deep_attr(o, root)
    result = [{key:mapper(item) for key,mapper in map} for item in item_list]
    return result


def create_path_map(mapping_def):
    map = [(key, get_deep_attr_getter(path)) for key, path in mapping_def.items()]
    return map

