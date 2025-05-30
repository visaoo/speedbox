import sqlite3
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from classes.order import Order


class PaymentMethod(Enum):
    PIX = 'pix'
    CARTAO = 'card'
    BOLETO = 'boleto'


class Status(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'


@dataclass
class Transaction:
    def __init__(self, payment_method: PaymentMethod, status: Status, order: Order) -> None:
        """
        Inicializa uma nova transação de pagamento.

        Args:
            payment_method (PaymentMethod): Método de pagamento utilizado.
            status (Status): Status atual da transação.
            order (Order): Objeto do pedido vinculado à transação.
        """
        self._created_at: datetime = datetime.now()
        self._status: Status = status
        self._value_total: float = order.value_total
        self._payment_method: PaymentMethod = payment_method

    @property
    def created_at(self) -> datetime:
        """Retorna a data e hora de criação da transação."""
        return self._created_at

    @property
    def status(self) -> Status:
        """Retorna o status atual da transação."""
        return self._status

    @status.setter
    def status(self, value: Status) -> None:
        """Define o status da transação."""
        self._status = value

    @property
    def value_total(self) -> float:
        """Retorna o valor total da transação."""
        return self._value_total

    @value_total.setter
    def value_total(self, value: float) -> None:
        """Define o valor total da transação."""
        self._value_total = value

    @property
    def payment_method(self) -> PaymentMethod:
        """Retorna o método de pagamento."""
        return self._payment_method

    @payment_method.setter
    def payment_method(self, value: PaymentMethod) -> None:
        """Define o método de pagamento."""
        self._payment_method = value

    def insert_transaction(self) -> None:
        """
        Insere a transação no banco de dados.
        """
        with sqlite3.connect("speedbox.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO transactions (payment_method, status, created_at)
                VALUES (?, ?, ?);
                """,
                (
                    self.payment_method.value,
                    self.status.value,
                    self.created_at.isoformat()
                ),
            )
            conn.commit()

    @staticmethod
    def get_by_id(transaction_id: int) -> Optional[tuple]:
        """
        Busca uma transação pelo ID no banco de dados.

        Args:
            transaction_id (int): ID da transação.

        Retorna:
            Optional[tuple]: Tupla com os dados da transação, se encontrada.
        """
        with sqlite3.connect("speedbox.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE id = ?;", (transaction_id,))
            return cursor.fetchone()

    @staticmethod
    def update_status(transaction_id: int, status: Status) -> None:
        """
        Atualiza o status de uma transação no banco de dados.

        Args:
            transaction_id (int): ID da transação.
            status (Status): Novo status a ser definido.
        """
        with sqlite3.connect("speedbox.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE transactions SET status = ? WHERE id = ?;",
                (status.value, transaction_id),
            )
            conn.commit()

    @staticmethod
    def delete(transaction_id: int) -> None:
        """
        Remove uma transação do banco de dados.

        Args:
            transaction_id (int): ID da transação a ser deletada.
        """
        with sqlite3.connect("speedbox.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM transactions WHERE id = ?;", (transaction_id,))
            conn.commit()

    def to_dict(self) -> dict:
        """
        Retorna a transação como um dicionário.

        Retorna:
            dict: Representação em dicionário da transação.
        """
        return {
            "created_at": self.created_at.isoformat(),
            "status": self.status.value,
            "value_total": self.value_total,
            "payment_method": self.payment_method.value
        }

    def __str__(self) -> str:
        """
        Retorna a representação textual da transação.

        Retorna:
            str: String com os dados da transação.
        """
        return (
            f"Transaction(created_at={self.created_at}, "
            f"status={self.status}, "
            f"value_total={self.value_total}, "
            f"payment_method={self.payment_method})"
        )
