from enum import Enum
from classes.address.address import Address

from uuid import uuid4

import sqlite3

class TypeKeyPix(Enum):
    EMAIL = 'email'
    UUID = 'UUID'
    CELPHONE = 'celphone'
    CNPJ = 'cnpj'
    CPF = 'cpf'
    
    
class Enterprise:
    def __init__(self, name: str, cnpj: str, address: Address):
        self._name = name
        self._cnpj = cnpj
        self._address = address
        self._type_key_pix = TypeKeyPix.CNPJ
        self._pix_key = self._cnpj
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def cnpj(self):
        return self._cnpj

    @cnpj.setter
    def cnpj(self, value):
        self._cnpj = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def type_key_pix(self):
        return self._type_key_pix
    
    @type_key_pix.setter
    def type_key_pix(self, value):
        if not isinstance(value, TypeKeyPix):
            raise ValueError("TypeKeyPix must be an instance of TypeKeyPix Enum")
        self._type_key_pix = value
        
        
    @property
    def pix_key(self):
        return self._pix_key
    
    @pix_key.setter
    def pix_key(self, value):
        if self._type_key_pix == TypeKeyPix.CPF:
            self._pix_key = value
        elif self._type_key_pix == TypeKeyPix.EMAIL:
            self._pix_key = value
        elif self._type_key_pix == TypeKeyPix.CELPHONE:
            self._pix_key = value
        elif self._type_key_pix == TypeKeyPix.UUID:
            self._pix_key = str(uuid4())
        else: 
            raise ValueError("Invalid TypeKeyPix")
        
    import sqlite3

    def insert(name, cnpj, user_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO enterprises (name, cnpj, user_id)
                VALUES (?, ?, ?);
            """, (name, cnpj, user_id))
            conn.commit()

    def get_all():
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM enterprises;")
            return cursor.fetchall()

    def get_by_id(enterprise_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM enterprises WHERE id = ?;", (enterprise_id,))
            return cursor.fetchone()

    def update(enterprise_id, name=None, cnpj=None, user_id=None):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            fields, values = [], []

            if name:
                fields.append("name = ?")
                values.append(name)
            if cnpj:
                fields.append("cnpj = ?")
                values.append(cnpj)
            if user_id:
                fields.append("user_id = ?")
                values.append(user_id)

            if not fields:
                return

            values.append(enterprise_id)
            query = f"UPDATE enterprises SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, values)
            conn.commit()

    def delete(enterprise_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM enterprises WHERE id = ?;", (enterprise_id,))
            conn.commit()
