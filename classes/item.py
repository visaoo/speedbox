from enum import Enum


class item_size(Enum):
    PEQUENO = 1
    MEDIO = 2
    GRANDE = 3


class Item:
    def __init__(self, name, price, type, description, size):
        self._name = name
        self._price = price
        self._type = type
        self._description = description
        self._size = size

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
