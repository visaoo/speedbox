from dataclasses import dataclass
import datetime
from tarfile import data_filter
from classes.order import Order
from classes.user.person import Person
from classes.user.user import User
from classes.address.address import Address
from typing import List

@dataclass
class Client(Person):
    def __init__(self, name: str, cpf:str, phone: str, birth_date: str, address: Address) -> None:
        super().__init__(name, cpf, address, birth_date)
        self._phone = phone
    
    @property
    def phone(self) -> str:
        return self._phone
    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = value
        
    def __str__(self) -> str:
        return f"Client: {self._name}, CPF: {self._cpf}, Phone: {self._phone}, Address: {self._address}, Birth Date: {self._birth_date}"
    
    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "cpf": self._cpf,
            "phone": self._phone,
            "address": self._address.to_dict(),
            "birth_date": self._birth_date
        }
    
    