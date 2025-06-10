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
        self._origem = origem
        self._destino  = destino
        self._date = datetime.now()
        self._status = status
        self._value_total = 15  # Valor base do pedido
        self._distance = distance
        
    @property
    def distance(self):
        return self._distance
    
    @distance.setter
    def distance(self, value):
        self._distance = value
        total = 15 + (value * 2)  # Valor base + R$2 por km
        self.value_total = total  # Atualiza o valor total com base na distância

    @property
    def origem(self):
        return self._origem

    @origem.setter
    def origem(self, value):
        self._origem = value

    @property
    def destino(self):
        return self._destino

    @destino.setter
    def destino(self, value):
        self._destino = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def value_total(self):
        return self._value_total
    
    @value_total.setter
    def value_total(self, value):
        self._value_total = value

    def insert(self, type_user: str, client_id=None, enterprise_id=None) -> None:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            # Certifique-se que self.origem e self.destino são do tipo Address e suportam str()
            origem = str(self.origem)
            destino = str(self.destino)

            if type_user == "enterprise":
                if enterprise_id is None:
                    raise ValueError("enterprise_id é obrigatório para pedidos de empresa.")
                cursor.execute("""
                    INSERT INTO orders_enterprises (total, date, addrss_final, addrss_initial, status, enterprise_id)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (
                    self.value_total,
                    self.date.isoformat(),
                    destino,
                    origem,
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
                    destino,
                    origem,
                    self.status.value,
                    client_id
                ))
            else:
                raise ValueError("Tipo de usuário inválido. Use 'enterprise' ou 'client'.")


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
        return f"Order({self.origem}, {self.destino}, {self.status}, {self.value_total})"
