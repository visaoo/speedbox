from abc import ABC, abstractmethod
from typing import Optional

from requests import get
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

    def __init__(self, name: str, cpf: str, address: Address, birth_date: str, user_id) -> None:
        self._name: str = name
        self._cpf: str = cpf
        self._address: Address = address
        self._birth_date: str = birth_date
        self._user_id = user_id
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

    @property
    def user_id(self) -> Optional[str]:
        """Retorna o ID do usuário."""
        return self._user_id
    
    @user_id.setter
    def user_id(self, value: str) -> None:
        self._user_id = value
        
    @abstractmethod
    def insert(self) -> None:
        """
        Método abstrato para inserir a pessoa no banco de dados.
        Deve ser implementado nas subclasses.
        """
        pass
    
    @abstractmethod
    def get_all() -> list:
        """
        Método abstrato para obter todas as pessoas do banco de dados.
        Deve ser implementado nas subclasses.
        """
        pass
    
    @abstractmethod
    def get_by_id():
        """
        Método abstrato para obter uma pessoa pelo ID.
        Deve ser implementado nas subclasses.
        """
        pass
    
    @abstractmethod
    def update():
        """
        Método abstrato para atualizar os dados da pessoa.
        Deve ser implementado nas subclasses.
        """
        pass
    
    
    @abstractmethod
    def delete():
        """
        Método abstrato para deletar a pessoa do banco de dados.
        Deve ser implementado nas subclasses.
        """
        pass