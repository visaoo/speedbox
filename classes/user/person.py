from datetime import datetime
from typing import List

from classes.address.address import Address
from abc import ABC

class Person(ABC):
    def __init__(self, name: str, cpf: str, address: List[Address], birth_date: datetime):
        self._name = name
        self._cpf = cpf
        self._address = address
        self._birth_date = birth_date

    @property
    def name(self):
        return self._name

    @property
    def cpf(self):
        return self._cpf

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def address(self):
        return self._address

    @property
    def birth_date(self):
        return self._birth_date
