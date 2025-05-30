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
        self.name: str = name
        self.cpf: str = cpf
        self.birth_date: str = birth_date
        self.cnh: str = cnh
        self.availability: bool = availability
        self.vehicle: Optional[Vehicle] = vehicle
        self.phone: str = phone
        self.address: Address = address
        self.user_id: int = user_id

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
