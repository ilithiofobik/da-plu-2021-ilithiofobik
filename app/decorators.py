from functools import wraps

#2.1
def greetings(callable):
    def inner():
        names = callable().split()
        word = "Hello"
        for name in names:
            word = word + " " + name.lower().capitalize()
        return word
    return inner


#2.2
def is_palindrome(callable):
    def inner():
        word = ''.join(filter(str.isalnum, callable())).lower()
        rev = word[::-1]
        if word == rev:
            return callable() + " - is palindrome"
        else:
            return callable() + " - is not palindrome"
    return inner


#2.3
def format_output(*args):
    def decorator(callable):
        nonlocal args
        def wrapper():
            nonlocal args
            indict = callable()
            outdict = {}
            for arg in args:
                names = arg.split("__")
                val = ""
                for name in names:
                    if name not in indict:
                        raise ValueError()
                    if val != "":
                        val += " "
                    val += indict[name]
                outdict[arg] = val
            return outdict
        return wrapper
    return decorator


#2.4
def add_class_method(cls):
    def decorator(func):
        @classmethod
        @wraps(func)
        def wrapper(self):
            return func()
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator


def add_instance_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self):
            return func()
        setattr(cls, func.__name__, wrapper)
        return func
    return decorator
