import sqlite3
from typing import Optional
from classes.user.user import User
from classes.Vehicle import Vehicle
from classes.address.address import Address

class DeliveryPerson:
    def __init__(
        self,
        name: str,
        cpf: str,
        birth_date: str,
        cnh: str,
        availability: bool,
        vehicle: Optional[Vehicle],
        user: User,
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
        self.user: User = user
        self.phone: str = phone
        self.address: Address = address
        self.user_id: int = user_id

    def insert(self) -> None:
        """
        Insere o entregador no banco de dados.
        """
        with sqlite3.connect("database.db") as conn:
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
        with sqlite3.connect("database.db") as conn:
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
