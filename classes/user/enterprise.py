import sqlite3
from enum import Enum
from typing import List, Optional
from uuid import uuid4

from classes.address.address import Address
from db.database import get_connection


class TypeKeyPix(Enum):
    EMAIL = 'email'
    UUID = 'uuid'
    PHONE = 'phone'
    CNPJ = 'cnpj'
    CPF = 'cpf'


class Enterprise:
    def __init__(self, name: str, cnpj: str, address: Address, user_id) -> None:
        """
        Inicializa uma empresa com nome, CNPJ e endereço.

        Args:
            name (str): Nome da empresa.
            cnpj (str): CNPJ da empresa.
            address (Address): Endereço da empresa.
        """
        self._name: str = name
        self._cnpj: str = cnpj
        self._address: Address = address
        self._type_key_pix: TypeKeyPix = TypeKeyPix.CNPJ
        self._pix_key: str = self._cnpj
        self.user_id = user_id

    @property
    def name(self) -> str:
        """Retorna o nome da empresa."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def cnpj(self) -> str:
        """Retorna o CNPJ da empresa."""
        return self._cnpj

    @cnpj.setter
    def cnpj(self, value: str) -> None:
        self._cnpj = value

    @property
    def address(self) -> Address:
        """Retorna o endereço da empresa."""
        return self._address

    @address.setter
    def address(self, value: Address) -> None:
        self._address = value

    @property
    def type_key_pix(self) -> TypeKeyPix:
        """Retorna o tipo da chave Pix da empresa."""
        return self._type_key_pix

    @type_key_pix.setter
    def type_key_pix(self, value: TypeKeyPix) -> None:
        if not isinstance(value, TypeKeyPix):
            raise ValueError("type_key_pix deve ser uma instância de TypeKeyPix.")
        self._type_key_pix = value

    @property
    def pix_key(self) -> str:
        """Retorna a chave Pix da empresa."""
        return self._pix_key

    @pix_key.setter
    def pix_key(self, value: Optional[str]) -> None:
        """
        Define a chave Pix com base no tipo.

        Args:
            value (str | None): Valor da chave Pix (ignorado se tipo for UUID).
        """
        if self._type_key_pix == TypeKeyPix.UUID:
            self._pix_key = str(uuid4())
        elif self._type_key_pix in {
            TypeKeyPix.CPF,
            TypeKeyPix.CNPJ,
            TypeKeyPix.EMAIL,
            TypeKeyPix.PHONE
        }:
            if not value:
                raise ValueError("Valor inválido para a chave Pix.")
            self._pix_key = value
        else:
            raise ValueError("Tipo de chave Pix inválido.")

    def insert(self) -> None:
        """
        Insere a empresa no banco de dados.
        """
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO enterprises (name, cnpj, user_id)
                VALUES (?, ?, ?);
            """, (self.name, self.cnpj, self.user_id))
            conn.commit()

    @staticmethod
    def get_all() -> List[tuple]:
        """
        Retorna todas as empresas cadastradas.

        Returns:
            List[tuple]: Lista de tuplas com os dados das empresas.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM enterprises;")
            return cursor.fetchall()

    @staticmethod
    def get_by_id(enterprise_id: int) -> Optional[tuple]:
        """
        Retorna uma empresa pelo ID.

        Args:
            enterprise_id (int): ID da empresa.

        Returns:
            Optional[tuple]: Dados da empresa.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM enterprises WHERE id = ?;", (enterprise_id,))
            return cursor.fetchone()

    @staticmethod
    def update(
        enterprise_id: int,
        name: Optional[str] = None,
        cnpj: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> None:
        """
        Atualiza os dados de uma empresa.

        Args:
            enterprise_id (int): ID da empresa.
            name (Optional[str]): Novo nome.
            cnpj (Optional[str]): Novo CNPJ.
            user_id (Optional[int]): ID do usuário associado.
        """
        with get_connection() as conn:
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

    @staticmethod
    def delete(enterprise_id: int) -> None:
        """
        Remove uma empresa do banco de dados.

        Args:
            enterprise_id (int): ID da empresa a ser removida.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM enterprises WHERE id = ?;", (enterprise_id,))
            conn.commit()
