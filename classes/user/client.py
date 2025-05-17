import datetime
from classes.item import Item
from classes.order import Order
from classes.user.person import Person
from classes.user.user import User
from classes.address.address import Address
from typing import List

from db import database

class Client(Person):
    def __init__(
        self,
        name: str,
        cpf: str,
        address: Address,
        birth_date: datetime,
        user: User,
    ):
        super().__init__(name, cpf, address, birth_date)

        self._order_history = [List[Order]]  # Lista de pedidos
        self._user = user

