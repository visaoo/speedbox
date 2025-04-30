import datetime
from typing import List
from endereco import Endereco 

class Pessoa:
    def __init__(self, nome: str, cpf: str, endereco: List[Endereco], data_nascimento: datetime.date) :
        self._nome = nome
        self._cpf = cpf
        self._endereco = endereco
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nascimento(self):
        return self._data_nascimento