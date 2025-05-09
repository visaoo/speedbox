from Address import Address
from enum import Enum


class TypeKeyPix(Enum):
    EMAIL = 'email'
    UUID = 'UUID'
    CELPHONE = 'celphone'
    CPF = 'CPF'
    CNPJ = 'cnpj'


class Enterprise:
    def __init__(self, name:str, cnpj:str, address:Address):
        self._name = name
        self._cnpj = cnpj
        self._address = address

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def cnpj(self):
        return self._cnpj

    @cnpj.setter
    def cnpj(self, value):
        self._cnpj = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

        
        