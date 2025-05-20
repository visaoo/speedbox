from enum import Enum

# Enum para OrderStatus (alinhado com o CHECK do banco)
class OrderStatus(Enum):
    PAYMENT_PENDING = "payment_pending"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"