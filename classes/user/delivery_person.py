from typing import List

from order import Order
from person import Person
from user import User
from Vehicle import Vehicle
from db.database import get_connection


import sqlite3

class DeliveryPerson(Person):
    def __init__(self, name, cpf, address, birth_date, cnh: None, available: bool, vehicle: Vehicle, user: User, phone: str) -> None:
        super().__init__(name, cpf, address, birth_date)
        self._cnh = cnh
        self._available = available
        self._vehicle = vehicle
        self._accepted_orders = []
        self.user = user
        self.phone = phone

    @property
    def cnh(self):
        return self._cnh

    @property
    def available(self):
        return self._available

    @available.setter
    def available(self, value):
        if not isinstance(value, bool):
            raise ValueError("O valor de 'available' deve ser um booleano.")
        self._available = value

    @property
    def vehicle(self):
        return self._vehicle

    @vehicle.setter
    def vehicle(self, value):
        self._vehicle = value

    @property
    def accepted_orders(self):
        return self._accepted_orders

    @accepted_orders.setter
    def accepted_orders(self, value):
        self._accepted_orders = value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value: User):
        self._user = value

    def insert(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO delivery_person (name, cpf, cnh,birth_date, celphone)
                VALUES (?, ?, ?, ?, ?);
            """, (self.name, self.cpf, self.birth_date, self.phone))
            conn.commit()
    @staticmethod
    def get_all():
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM delivery_person;")
            return cursor.fetchall()
        
    @staticmethod
    def get_by_id(person_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM delivery_person WHERE id = ?;", (person_id,))
            return cursor.fetchone()

    @staticmethod
    def update(person_id, name=None, cpf=None, user_id=None, birth_date=None, celphone=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            fields, values = [], []

            if name:
                fields.append("name = ?")
                values.append(name)
            if cpf:
                fields.append("cpf = ?")
                values.append(cpf)
            if user_id:
                fields.append("user_id = ?")
                values.append(user_id)
            if birth_date:  
                fields.append("birth_date = ?")
                values.append(birth_date)
            if celphone:
                fields.append("celphone = ?")
                values.append(celphone)
            if not fields:
                return

            values.append(person_id)
            query = f"UPDATE delivery_person SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, values)
            conn.commit()
            
    @staticmethod
    def delete(person_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM delivery_person WHERE id = ?;", (person_id,))
            conn.commit()
