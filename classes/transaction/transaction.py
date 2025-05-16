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


class Transaction:
    def __init__(self, payment_method: PaymentMethod, status: Status, created_at: datetime = None):
        if created_at is None:
            created_at = datetime.now()
        self._created_at = created_at
        self._status = status
        self._value_total = Order.value_total
        self._payment_method = payment_method
        
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
