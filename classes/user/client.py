from typing import Any, List, Optional

from classes.address.address import Address
from classes.user.person import Person
from db.database import get_connection

import sqlite3

class Client(Person):
    def __init__(
        self,
        name: str,
        cpf: str,
        phone: str,
        birth_date: str,
        address: Address,
        user_id,
    ) -> None:
        """
        Inicializa um cliente com nome, CPF, telefone, data de nascimento e endereço.

        Args:
            name (str): Nome completo do cliente.
            cpf (str): CPF do cliente.
            phone (str): Telefone de contato.
            birth_date (str): Data de nascimento no formato 'YYYY-MM-DD'.
            address (Address): Endereço associado ao cliente.
        """
        super().__init__(name, cpf, address, birth_date, user_id)
        self._phone: str = phone

    @property
    def phone(self) -> str:
        """Retorna o telefone do cliente."""
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        """Atualiza o telefone do cliente."""
        self._phone = value

    def insert(self) -> None:
        """
        Insere o cliente no banco de dados.
        """
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    INSERT INTO clients (name, cpf, birth_date, celphone, user_id)
                    VALUES (?, ?, ?, ?, ?);
                    """,
                    (self.name, self.cpf, self.birth_date, self.phone, self.user_id),
                )
                conn.commit()
        except sqlite3.IntegrityError as e:
            print(f'Erro ao inserir cliente: {e}')

    @staticmethod
    def get_all() -> List[Any]:
        """
        Retorna todos os clientes cadastrados no banco de dados.

        Returns:
            List[Any]: Lista de tuplas com os dados dos clientes.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients;")
            return cursor.fetchall()

    @staticmethod
    def get_by_id(client_id: int) -> Optional[Any]:
        """
        Retorna um cliente específico pelo ID.

        Args:
            client_id (int): ID do cliente.

        Returns:
            Optional[Any]: Dados do cliente, se encontrado.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE id = ?;", (client_id,))
            return cursor.fetchone()

    @staticmethod
    def update(
        client_id: int,
        name: Optional[str] = None,
        cpf: Optional[str] = None,
        birth_date: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> None:
        """
        Atualiza os dados de um cliente no banco de dados.

        Args:
            client_id (int): ID do cliente.
            name (Optional[str]): Novo nome.
            cpf (Optional[str]): Novo CPF.
            birth_date (Optional[str]): Nova data de nascimento.
            phone (Optional[str]): Novo telefone.
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
                return  # Nenhum campo foi fornecido para atualização

            values.append(client_id)
            query = f"UPDATE clients SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, values)
            conn.commit()

    @staticmethod
    def delete(client_id: int) -> None:
        """
        Remove um cliente do banco de dados.

        Args:
            client_id (int): ID do cliente a ser removido.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?;", (client_id,))
            conn.commit()

    def __str__(self) -> str:
        """Retorna uma representação textual do cliente."""
        return (
            f"Client: {self._name}, CPF: {self._cpf}, "
            f"Phone: {self._phone}, Address: {self._address}, "
            f"Birth Date: {self._birth_date}"
        )

    def to_dict(self) -> dict:
        """
        Retorna os dados do cliente como um dicionário.

        Returns:
            dict: Dicionário com os dados do cliente.
        """
        return {
            "name": self._name,
            "cpf": self._cpf,
            "phone": self._phone,
            "address": self._address.to_dict(),
            "birth_date": self._birth_date,
        }
