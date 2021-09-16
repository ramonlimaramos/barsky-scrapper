

__all__ = ['Employee']


class Employee:

    def __init__(self, name, raiting):
        self._name = name
        self._rating = raiting

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield(attr.replace('_', ''), value)

    def __repr__(self):
        return f'<Employee {self._name}>'
