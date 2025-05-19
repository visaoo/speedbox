from dataclasses import dataclass
import datetime
from tarfile import data_filter
from classes.order import Order
from classes.user.person import Person
from classes.user.user import User
from classes.address.address import Address
from typing import List

import sqlite3


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
    
    def insert(name, cpf, birth_date, celphone,user_id):
        """
        Função para inserir um cliente no banco de dados.
        """
        with sqlite3.connect("../database.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO clients (name, cpf, birth_date, celphone, user_id)
                VALUES (?, ?, ?, ?, ?);
                """,
                (name, cpf, birth_date, celphone, user_id),
            )
            conn.commit()

    def get_all():
        """
        Função para obter todos os clientes do banco de dados.
        """
        with sqlite3.connect("../database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients;")
            clients = cursor.fetchall()
        return clients

    def get_by_id(client_id):
        """
        Função para obter um cliente pelo ID.
        """
        with sqlite3.connect("../database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE id = ?;", (client_id,))
            client = cursor.fetchone()
        return client

    def update(client_id, name=None, cpf=None, birth_date=None, celphone=None):
        """
        Função para atualizar um cliente no banco de dados.
        """
        with sqlite3.connect("../database.db") as conn:
            cursor = conn.cursor()

            fields = []
            values = []

            if name:
                fields.append("name = ?")
                values.append(name)
            if cpf:
                fields.append("cpf = ?")
                values.append(cpf)
            if birth_date:
                fields.append("birth_date = ?")
                values.append(birth_date)
            if celphone:
                fields.append("celphone = ?")
                values.append(celphone)
            if not fields:
                return  # Nenhum campo para atualizar

            values.append(client_id)
            query = f"UPDATE clients SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, values)
            conn.commit()

    def delete(client_id):
        """
        Função para deletar um cliente do banco de dados.
        """
        with sqlite3.connect("../database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?;", (client_id,))
            conn.commit()

        
       
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
    
    