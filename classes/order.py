from enum import Enum, auto
from datetime import datetime
from typing import Union

from db.database import get_connection
from classes.address.address import Address
import sqlite3


class OrderStatus(Enum):
    """Enumeração para os possíveis status de um pedido."""
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()


class Order:
    """
    Classe que representa um pedido de entrega.

    Atributos:
        origem (Address): Endereço de origem.
        destino (Address): Endereço de destino.
        description (str): Descrição do pedido.
        status (OrderStatus): Status atual do pedido.
        value_total (float): Valor do pedido.
        date (datetime): Data de criação do pedido.
    """

    def __init__(self, origem: Address, destino: Address, description: str, status: OrderStatus) -> None:
        if not isinstance(description, str):
            raise ValueError("Descrição deve ser uma string.")
        if not isinstance(origem, Address):
            raise ValueError("Origem deve ser um endereço válido.")
        if not isinstance(destino, Address):
            raise ValueError("Destino deve ser um endereço válido.")
        if not isinstance(status, OrderStatus):
            raise ValueError("Status deve ser uma instância de OrderStatus.")

        self._origem = origem
        self._destino = destino
        self._description = description
        self._status = status
        self._value_total = 15.0  # Pode ser ajustado por distância
        self._date = datetime.now()

    @property
    def origem(self) -> Address:
        return self._origem

    @origem.setter
    def origem(self, value: Address) -> None:
        self._origem = value

    @property
    def destino(self) -> Address:
        return self._destino

    @destino.setter
    def destino(self, value: Address) -> None:
        self._destino = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def status(self) -> OrderStatus:
        return self._status

    @status.setter
    def status(self, value: OrderStatus) -> None:
        if not isinstance(value, OrderStatus):
            raise ValueError("Status deve ser uma instância de OrderStatus.")
        self._status = value

    @property
    def value_total(self) -> float:
        return self._value_total

    @value_total.setter
    def value_total(self, value: float) -> None:
        if not isinstance(value, float):
            raise ValueError("O valor total deve ser um número decimal (float).")
        self._value_total = value

    @property
    def date(self) -> datetime:
        return self._date

    def insert(self, type_user: str) -> None:
        """
        Insere o pedido no banco de dados de acordo com o tipo de usuário.

        Args:
            type_user (str): "enterprise" ou "client"
        """
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()

            if type_user == "enterprise":
                cursor.execute("""
                    INSERT INTO orders_enterprises (total, date, addrss_final, addrss_initial, status, description)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (
                    self.value_total,
                    self.date.isoformat(),
                    str(self.destino),
                    str(self.origem),
                    self.status.name,
                    self.description
                ))

            elif type_user == "client":
                cursor.execute("""
                    INSERT INTO orders (total, date, addrss_final, addrss_initial, status, description)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (
                    self.value_total,
                    self.date.isoformat(),
                    str(self.destino),
                    str(self.origem),
                    self.status.name,
                    self.description
                ))
            else:
                raise ValueError("Tipo de usuário inválido. Use 'enterprise' ou 'client'.")

            conn.commit()

    @staticmethod
    def get_by_enterprise(enterprise_id: int):
        """Retorna todos os pedidos de uma empresa pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders_enterprises WHERE enterprise_id = ?;", (enterprise_id,))
            return cursor.fetchall()

    @staticmethod
    def get_by_client(client_id: int):
        """Retorna todos os pedidos de um cliente pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE client_id = ?;", (client_id,))
            return cursor.fetchall()
        
    @staticmethod
    def get_by_id(user_id: int, user_type: str):
        with get_connection() as conn:
            cursor = conn.cursor()
            if user_type == "enterprise":
                table = 'orders_enterprises'
            elif user_type == "client":
                table = 'orders'
            else:
                raise ValueError("Tipo de usuário inválido. Use 'enterprise' ou 'client'.")

            cursor.execute(f"SELECT id FROM {table} WHERE id = ?;", (user_id,))
            return cursor.fetchall()


    @staticmethod
    def update_delivery_person(user_type: str, order_id: int, delivery_person_id: int) -> None:
        """Atualiza o entregador associado a um pedido."""
        with get_connection() as conn:
            cursor = conn.cursor()
            table = "orders_enterprises" if user_type == "enterprise" else "orders"
            cursor.execute(
                f"UPDATE {table} SET delivery_person_id = ? WHERE id = ?;",
                (delivery_person_id, order_id)
            )
            conn.commit()

    @staticmethod
    def update_status(order_id: int, new_status: OrderStatus, user_type: str) -> None:
        """Atualiza o status de um pedido."""
        if not isinstance(new_status, OrderStatus):
            raise ValueError("new_status deve ser uma instância de OrderStatus.")

        with get_connection() as conn:
            cursor = conn.cursor()
            table = "orders_enterprises" if user_type == "enterprise" else "orders"
            cursor.execute(
                f"UPDATE {table} SET status = ? WHERE id = ?;",
                (new_status.name, order_id)
            )
            conn.commit()

    @staticmethod
    def delete_order(order_id: int, user_type: str) -> None:
        """Deleta um pedido do banco de dados."""
        with get_connection() as conn:
            cursor = conn.cursor()
            table = "orders_enterprises" if user_type == "enterprise" else "orders"
            cursor.execute(f"DELETE FROM {table} WHERE id = ?;", (order_id,))
            conn.commit()
