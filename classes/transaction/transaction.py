from dataclasses import dataclass
from datetime import datetime
from enum import Enum

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
    def __init__(self, payment_method: PaymentMethod, status: Status, Order: Order):
        created_at = datetime.now()
        self._created_at = created_at
        self._status = status
        self._value_total = Order.value_total
        self._payment_method = payment_method
        

    @property
    def created_at(self):
        return self._created_at

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

    @property
    def payment_method(self):
        return self._payment_method

    @payment_method.setter
    def payment_method(self, value):
        self._payment_method = value

    def to_dict(self):
        return {
            "created_at": self._created_at,
            "status": self._status,
            "value_total": self._value_total,
            "payment_method": self._payment_method
        }
    
    def __str__(self):
        return f"Transaction(created_at={self._created_at}, status={self._status}, value_total={self._value_total}, payment_method={self._payment_method})"