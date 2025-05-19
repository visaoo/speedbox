from enum import Enum, auto

from classes import user
from classes.address.address import Address

import sqlite3

class OrderStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()

class Order:
    def __init__(self, origem: Address, status: OrderStatus, destino: Address, description: str) -> None:
        """
        Classe que representa um pedido de entrega.
        :param id: ID do pedido
        :param origem: Endereço de origem
        :param status: Status do pedido (Pendente, Em andamento, Concluído, Cancelado)
        :param destino: Endereço de destino
        """
        if not isinstance(description, str):
            raise ValueError("Descrição deve ser uma string")
        if not isinstance(origem, str):
            raise ValueError("Origem deve ser uma string")
        if not isinstance(status, OrderStatus):
            raise ValueError("Status deve ser um valor do enum OrderStatus")
        if not isinstance(destino, str):
            raise ValueError("Destino deve ser uma string")
        if status not in OrderStatus:
            raise ValueError("Status deve ser um valor do enum OrderStatus")
        self._description = description
        self._origem = origem
        self._status = status
        self._destino = destino
        self._value_total = 15.0  # Valor fixo do pedido, vai aumentar de acordo com a distancia

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        self._description = value
        
    @property
    def origem(self):
        return self._origem

    @property
    def status(self):
        return self._status

    @property
    def destino(self):
        return self._destino

    @status.setter
    def status(self, value):
        if not isinstance(value, OrderStatus):
            raise ValueError("Status deve ser um valor do enum OrderStatus")
        self._status = value

    @destino.setter
    def destino(self, value):
        self._destino = value
        
    @property
    def value_total(self):
        return self._value_total
    
    @value_total.setter
    def value_total(self, value):
        if not isinstance(value, float):
            raise ValueError("Valor total deve ser um número float")
        self._value_total = value
    

    def insert(self, type_user):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            if type_user == "enterprise":
                cursor.execute("""
                    INSERT INTO orders_enterprises (total, date, enterprise_id, delivery_person_id, addrss_final, addrss_initial, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?);
                """, (self.total, self.date, self.enterprise_id, self.delivery_person_id, self.addrss_final, self.addrss_initial, self.status))
                conn.commit()
            if type_user == "client":
                cursor.execute("""
                    INSERT INTO orders (total, date, client_id, delivery_person_id, addrss_final, addrss_initial, description,status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """, (self.total, self.date, self.client_id, self.delivery_person_id, self.addrss_final, self.addrss_initial, self.description,self.status))
                conn.commit()
                
    def get_by_enterprise(enterprise_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders_enterprises WHERE enterprise_id = ?;", (enterprise_id,))
            return cursor.fetchall()

    def get_by_client(client_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM orders WHERE client_id = ?;", (client_id,))
            return cursor.fetchall()

    
    def update_delivery_person(user_type, id, delivery_person_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            if user_type == "enterprise":
                cursor.execute("UPDATE orders_enterprises SET delivery_person_id = ? WHERE id = ?;", (delivery_person_id, id))
                conn.commit()
            elif user_type == "client":
                cursor.execute("UPDATE orders SET delivery_person_id = ? WHERE id = ?;", (delivery_person_id, id))
                conn.commit()


    def update_status(id, new_status, user_type):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            if user_type == "enterprise":
                cursor.execute("UPDATE orders_enterprises SET status = ? WHERE id = ?;", (new_status, id))
                conn.commit()
            elif user_type == "client":
                cursor.execute("UPDATE orders SET status = ? WHERE id = ?;", (new_status, id))
                conn.commit()


    def delete_order(id, user_type):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            if user_type == "enterprise":
                cursor.execute("DELETE FROM orders_enterprises WHERE id = ?;", (id,))
                conn.commit()
            elif user_type == "client":
                cursor.execute("DELETE FROM orders WHERE id = ?;", (id,))
                conn.commit()