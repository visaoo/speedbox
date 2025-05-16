from enum import Enum
from classes.address.address import Address

from uuid import uuid4

class TypeKeyPix(Enum):
    EMAIL = 'email'
    UUID = 'UUID'
    CELPHONE = 'celphone'
    CNPJ = 'cnpj'


class Enterprise:
    def __init__(self, name: str, cnpj: str, address: Address):
        self._name = name
        self._cnpj = cnpj
        self._address = address
        self._type_key_pix = TypeKeyPix.CNPJ
        self._pix_key = self._cnpj
        
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

    @property
    def type_key_pix(self):
        return self._type_key_pix
    
    @type_key_pix.setter
    def type_key_pix(self, value):
        if not isinstance(value, TypeKeyPix):
            raise ValueError("TypeKeyPix must be an instance of TypeKeyPix Enum")
        self._type_key_pix = value
        
        
    @property
    def pix_key(self):
        return self._pix_key
    
    @pix_key.setter
    def pix_key(self, value):
        if self._type_key_pix == TypeKeyPix.CPF:
            self._pix_key = value
        elif self._type_key_pix == TypeKeyPix.EMAIL:
            self._pix_key = value
        elif self._type_key_pix == TypeKeyPix.CELPHONE:
            self._pix_key = value
        elif self._type_key_pix == TypeKeyPix.UUID:
            self._pix_key = str(uuid4())
        else: 
            raise ValueError("Invalid TypeKeyPix")