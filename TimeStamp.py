import datetime as dt
from functools import wraps

def logged(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        time = dt.datetime.now()
        result = fn(*args, **kwargs)
        args_str = ', '.join(repr(arg) for arg in args)
        kwargs_str = ', '.join(f"{key}={repr(value)}" for key, value in kwargs.items())
        all_args = ', '.join(filter(None, [args_str, kwargs_str]))
        with open("LOGS.txt", "a") as file:
            file.write(f"{time}: {fn.__name__}({all_args}) ---> {result!r}\n")
        #print(f"{fn.__name__}({all_args}) invoked at {time} ---> {result!r}\n")
        return result
    return inner
