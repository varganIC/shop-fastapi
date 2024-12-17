

def decorator(name):
    def wrapper(K):
        setattr(K, name, eval(name))
        return K

    return wrapper


def _asdict(self):
    return self.__dict__
