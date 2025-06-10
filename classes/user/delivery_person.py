import sqlite3
from typing import Optional

from classes.address.address import Address
from classes.Vehicle import Vehicle


class DeliveryPerson:
    def __init__(
        self,
        name: str,
        cpf: str,
        birth_date: str,
        cnh: str,
        availability: bool,
        vehicle: Optional[Vehicle],
        phone: str,
        address: Address,
        user_id: int
    ) -> None:
        self._name: str = name
        self._cpf: str = cpf
        self._birth_date: str = birth_date
        self._cnh: str = cnh
        self._availability: bool = availability
        self._vehicle: Optional[Vehicle] = vehicle
        self._phone: str = phone
        self._address: Address = address
        self._user_id: int = user_id


    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def cpf(self) -> str:
        return self._cpf

    @cpf.setter
    def cpf(self, value: str):
        self._cpf = value

    @property
    def birth_date(self) -> str:
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: str):
        self._birth_date = value

    @property
    def cnh(self) -> str:
        return self._cnh

    @cnh.setter
    def cnh(self, value: str):
        self._cnh = value

    @property
    def availability(self) -> bool:
        return self._availability

    @availability.setter
    def availability(self, value: bool):
        self._availability = value

    @property
    def vehicle(self) -> Optional['Vehicle']:
        return self._vehicle

    @vehicle.setter
    def vehicle(self, value: Optional['Vehicle']):
        self._vehicle = value

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str):
        self._phone = value

    @property
    def address(self) -> 'Address':
        return self._address

    @address.setter
    def address(self, value: 'Address'):
        self._address = value

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value: int):
        self._user_id = value




    def insert(self) -> None:
        """
        Insere o entregador no banco de dados.
        """
        with sqlite3.connect("speedbox.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO delivery_person (name, cpf, cnh, birth_date, phone, user_id)
                VALUES (?, ?, ?, ?, ?, ?);
                """,
                (self.name, self.cpf, self.cnh, self.birth_date, self.phone, self.user_id)
            )
            conn.commit()

    @staticmethod
    def get_by_id(id: int):
        with sqlite3.connect("speedbox.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, name, cpf, cnh, birth_date, phone, user_id
                FROM delivery_person
                WHERE id = ?;
                """,
                (id,)
            )
            return cursor.fetchone()

    def __str__(self) -> str:
        return (f'Entregador: {self.name}' f'CNH: {self.cnh}'
                f'data de nascimento: {self.birth_date}'
                f'CPF: {self.cpf}' f'telefone: {self.phone}')
