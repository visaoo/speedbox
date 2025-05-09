from sqlalchemy import (Column, Integer, ForeignKey, String, DateTime)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


class Boleto(Base):
    __tablename__ = 'boleto'
    
    transaction_id = Column(Integer, ForeignKey('transactions.id'), primary_key=True)
    code_bar = Column(String(100))
    expiration = Column(DateTime)
    
    transaction = relationship('Transaction', back_populates='boleto')
    
    def __init__(self, code_bar, typeable_line):
        self._code_bar = code_bar
        self._typeable_line = typeable_line


    @property
    def code_bar(self):
        return self._code_bar

    @code_bar.setter
    def code_bar(self, value):
        self._code_bar = value

    @property
    def typeable_line(self):
        return self._typeable_line

    @typeable_line.setter
    def typeable_line(self, value):
        self._typeable_line = value

