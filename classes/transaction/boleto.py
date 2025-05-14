from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Boleto(Base):
    __tablename__ = 'boleto'

    transaction_id = Column(Integer, ForeignKey('transactions.id'), primary_key=True)
    code_bar = Column(String(100))
    expiration = Column(DateTime)

    transaction = relationship('Transaction', back_populates='boleto')

    def __init__(self, typeable_line):
        self._typeable_line = typeable_line

    @property
    def typeable_line(self):
        return self._typeable_line

    @typeable_line.setter
    def typeable_line(self, value):
        self._typeable_line = value
