class Path:
    def __init__(self, path=''):
        self._path = path

    def __str__(self):
        return self._path

    def __repr__(self):
        return "{} <{}>".format(self.__class__.__name__, str(self))

    def __truediv__(self, other):
        # TODO: Replace stub with something more useful
        return self

    def exists(self):
        # TODO: Replace stub with something more useful
        return True


class Paths:
    @property
    def app(self):
        return Path()


paths = Paths()
