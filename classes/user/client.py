from dataclasses import dataclass
from turtle import st
from classes.user.person import Person
from classes.address.address import Address

import sqlite3

from db.database import get_connection


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
    
    def insert(self):
        """
        Função para inserir um cliente no banco de dados.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO clients (name, cpf, birth_date, phone)
                VALUES (?, ?, ?, ?);
                """,
                (self.name, self.cpf, self.birth_date, self.phone),
            )
            conn.commit()
            
    @staticmethod
    def get_all():
        """
        Função para obter todos os clientes do banco de dados.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients;")
            clients = cursor.fetchall()
        return clients
    
    @staticmethod
    def get_by_id(client_id):
        """
        Função para obter um cliente pelo ID.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE id = ?;", (client_id,))
            client = cursor.fetchone()
        return client
    
    @staticmethod
    def update(client_id, name=None, cpf=None, birth_date=None, phone=None):
        """
        Função para atualizar um cliente no banco de dados.
        """
        with get_connection() as conn:
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
            if phone:
                fields.append("phone = ?")
                values.append(phone)
            if not fields:
                return  # Nenhum campo para atualizar

            values.append(client_id)
            query = f"UPDATE clients SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, values)
            conn.commit()
    @staticmethod
    def delete(client_id):
        """
        Função para deletar um cliente do banco de dados.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?;", (client_id,))
            conn.commit()

        
       
    def __str__(self) -> str:
        return f"Client: {self._name}, CPF: {self._cpf}, phone: {self._phone}, Address: {self._address}, Birth Date: {self._birth_date}"
    
    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "cpf": self._cpf,
            "phone": self._phone,
            "address": self._address.to_dict(),
            "birth_date": self._birth_date
        }
    
    