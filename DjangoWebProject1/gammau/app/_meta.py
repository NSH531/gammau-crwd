class _meta:
    pass

def dict_to_class(dictionary):
    obj = _meta()
    for key, value in dictionary.items():
        setattr(obj, key, value)
    return obj
