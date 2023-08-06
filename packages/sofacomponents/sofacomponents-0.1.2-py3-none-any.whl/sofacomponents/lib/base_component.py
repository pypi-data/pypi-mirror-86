import functools


def sofa_component(func):
    @functools.wraps(func)
    def wrapper_sofa_component(*args, **kwargs):
        defaults = dict(args[0]._defaults)
        infos = func(*args, **kwargs)
        name, _defaults = infos if len(infos) == 2 else (infos, dict())
        defaults.update(_defaults)
        defaults.update(kwargs)
        return name, defaults

    return wrapper_sofa_component
