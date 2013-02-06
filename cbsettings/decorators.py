from functools import wraps


def _create_method_wrapper(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper


def callable_setting(fn=None, takes_self=True):
    def decorator(fn):
        if not takes_self:
            fn = _create_method_wrapper(fn)
        fn.is_callable_setting = True
        return fn

    if fn is None:
        return decorator
    else:
        return decorator(fn)
