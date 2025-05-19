from abc import ABC
from typing import Optional
from classes.address.address import Address


class Person(ABC):
    """
    Classe abstrata que representa uma pessoa.

    Atributos:
        name (str): Nome completo da pessoa.
        cpf (str): CPF da pessoa.
        address (Address): Endereço da pessoa.
        birth_date (str): Data de nascimento da pessoa no formato ISO (YYYY-MM-DD).
    """

    def __init__(self, name: str, cpf: str, address: Address, birth_date: str) -> None:
        self._name: str = name
        self._cpf: str = cpf
        self._address: Address = address
        self._birth_date: str = birth_date

    @property
    def name(self) -> str:
        """Retorna o nome da pessoa."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def cpf(self) -> str:
        """Retorna o CPF da pessoa."""
        return self._cpf

    @property
    def address(self) -> Address:
        """Retorna o endereço da pessoa."""
        return self._address

    @address.setter
    def address(self, value: Address) -> None:
        self._address = value

    @property
    def birth_date(self) -> str:
        """Retorna a data de nascimento da pessoa."""
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: str) -> None:
        self._birth_date = value
