from enum import Enum, auto

import classes.AddressClient as AddressClient


class OrderStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()


class Order:
    def __init__(self, id: int, origem: AddressClient, status: OrderStatus, destino: AddressClient) -> dict:
        """
        Classe que representa um pedido de entrega.
        :param id: ID do pedido
        :param origem: Endereço de origem
        :param status: Status do pedido (Pendente, Em andamento, Concluído, Cancelado)
        :param destino: Endereço de destino
        """
        if not isinstance(id, int):
            raise ValueError("ID deve ser um número inteiro")
        if not isinstance(origem, str):
            raise ValueError("Origem deve ser uma string")
        if not isinstance(status, OrderStatus):
            raise ValueError("Status deve ser um valor do enum OrderStatus")
        if not isinstance(destino, str):
            raise ValueError("Destino deve ser uma string")
        if status not in OrderStatus:
            raise ValueError("Status deve ser um valor do enum OrderStatus")

        self._id = id
        self._origem = origem
        self._status = status
        self._destino = destino

    @property
    def id(self):
        return self._id

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

    def nextStatus(self):
        if self._status == OrderStatus.PENDING:
            self._status = OrderStatus.IN_PROGRESS
        elif self._status == OrderStatus.IN_PROGRESS:
            self._status = OrderStatus.COMPLETED
        elif self._status == OrderStatus.COMPLETED:
            self._status = OrderStatus.CANCELLED
        else:
            raise ValueError("Pedido já cancelado")

    def __str__(self):
        return f"Pedido({self._id=}, {self._origem=}, {self._status=}, {self._destino=})"


# Testando a classe Order
pedido = Order(1, "Rua Folha Dourada, 6, Jardim Miragaia, São Paulo, SP", OrderStatus.PENDING, "Rua Olivio Segatto, 1017, Centro, Tupi Paulista, SP")
print(pedido)  # Pendente
pedido.nextStatus()
print(pedido)  # Em andamento
pedido.nextStatus()
print(pedido)  # Concluído
pedido.nextStatus()
print(pedido)  # Cancelado
