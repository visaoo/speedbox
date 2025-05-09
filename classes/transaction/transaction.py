from sqlalchemy import (Column, Integer, ForeignKey, DateTime, Numeric, Enum)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from enum import Enum

Base = declarative_base()

class PaymentMethod(Enum):
    PIX = 'pix'
    CARTAO = 'cartao'
    BOLETO = 'boleto'
    
class Transaction(Base):
    __tablename__ = 'transactions'
    
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    value = Column(Numeric(10, 2))
    date = Column(DateTime, default=datetime.utcnow)
    type_payment = Column(Enum(PaymentMethod))
    
    pedido = relationship("Pedido", back_populates="transacao")
    pix = relationship("Pix", uselist=False, back_populates="transacao")
    cartao = relationship("Cartao", uselist=False, back_populates="transacao")
    boleto = relationship("Boleto", uselist=False, back_populates="transacao")


# adicionar __init__ para validações.

