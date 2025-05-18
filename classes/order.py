from enum import Enum, auto

from Veihcle import Vehicle
from classes.address.address import Address

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
        
    def to_dict(self) -> dict:
        """
        Método para converter o pedido em um dicionário.
        :return: Dicionário com os dados do pedido
        """
        return {
            "origem": self._origem,
            "status": self._status.name,
            "destino": self._destino,
            "value_total": self._value_total
        }
        
    def __str__(self):
        return f"Order({self._origem}, {self._status}, {self._destino}, {self._value_total})"


# Testando a classe Order
# pedido = Order(1, "Rua Folha Dourada, 6, Jardim Miragaia, São Paulo, SP", OrderStatus.PENDING, "Rua Olivio Segatto, 1017, Centro, Tupi Paulista, SP")
# print(pedido)  # Pendente
# pedido.nextStatus()
# print(pedido)  # Em andamento
# pedido.nextStatus()
# print(pedido)  # Concluído
# pedido.nextStatus()
# print(pedido)  # Cancelado