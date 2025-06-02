import sqlite3
from datetime import datetime
from enum import Enum
from classes.product import Product
from app.utils.get_connection import get_connection
from classes.address.address import Address


class OrderStatus(Enum):
    PAYMENT_PENDING = "payment_pending"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"


class Order:
    def __init__(self, origem: Address, destino: Address, status: OrderStatus, distance=0) -> None:
        self.origem: Address = origem
        self.destino: Address = destino
        self.date: datetime = datetime.now()
        self.status: OrderStatus = status
        self.value_total: float = round(10 + (float(distance) * 0.5), 2)  # Valor base de 15 + valor por km

    def insert(self, type_user: str, client_id=None, enterprise_id=None) -> None:
        """
        Insere o pedido no banco de dados de acordo com o tipo de usuário.

        Args:
            type_user (str): "enterprise" ou "client"
            client_id (int, optional): ID do cliente para pedidos de cliente
            enterprise_id (int, optional): ID da empresa para pedidos de empresa
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            if type_user == "enterprise":
                if enterprise_id is None:
                    raise ValueError("enterprise_id é obrigatório para pedidos de empresa.")
                cursor.execute("""
                    INSERT INTO orders_enterprises (total, date, addrss_final, addrss_initial, status, enterprise_id)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (
                    self.value_total,
                    self.date.isoformat(),
                    str(self.destino),
                    str(self.origem),
                    self.status.value,
                    enterprise_id
                ))

            elif type_user == "client":
                if client_id is None:
                    raise ValueError("client_id é obrigatório para pedidos de cliente.")
                cursor.execute("""
                    INSERT INTO orders (total, date, addrss_final, addrss_initial, status, client_id)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (
                    self.value_total,
                    self.date.isoformat(),
                    str(self.destino),
                    str(self.origem),
                    self.status.value,
                    client_id
                ))
            else:
                raise ValueError("Tipo de usuário inválido. Use 'enterprise' ou 'client'.")

            conn.commit()

    @staticmethod
    def update_delivery_person(type_user: str, order_id: int, delivery_person_id: int) -> None:
        table = "orders" if type_user == "client" else "orders_enterprises"
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE {table}
                SET delivery_person_id = ?
                WHERE id = ?;
            """, (delivery_person_id, order_id))
            conn.commit()

    @staticmethod
    def update_status(order_id: int, status: OrderStatus, type_user: str) -> None:
        table = "orders" if type_user == "client" else "orders_enterprises"
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE {table}
                SET status = ?
                WHERE id = ?;
            """, (status.value, order_id))
            conn.commit()

    @staticmethod
    def get_by_client(client_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM orders
                WHERE client_id = ?;
            """, (client_id,))
            return cursor.fetchall()

    @staticmethod
    def get_by_id(user_id: int, user_type: str):
        with sqlite3.connect('speedbox.db') as conn:
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
    def get_by_enterprise(enterprise_id: int):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT *
                FROM orders_enterprises
                WHERE enterprise_id = ?;
            """, (enterprise_id,))
            return cursor.fetchall()

    
    def get_id(self, type_user:str):
        """
        
        """
        try:
            if type_user == 'client':
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                                SELECT id FROM orders WHERE addrss_final=? AND addrss_initial=?
                                AND date=?
                                """, (self.destino, self.origem, self.date))
            elif type_user == 'enterprise':
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("""
                                SELECT id FROM orders_enterprises WHERE addrss_final=? AND addrss_initial=?
                                AND date=?
                                """, (self.destino, self.origem, self.date))
            else:
                raise
        except Exception as e:
            print(f'Erro: [{e}]')
        
    
    
    def __str__(self):
        return f"Order({self.origem}, {self.destino}, {self.description}, {self.status}, {self.value_total})"
