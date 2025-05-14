from sqlalchemy import (Column, Integer, String)
from db.database import Base

class AddressBase(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    _street = Column(String(100))
    _number = Column(Integer)
    _neighborhood = Column(String(50))
    _city = Column(String(25))
    _state = Column(String(20))
    
    
    def __str__(self):
        return f'{self.rua}, {self.numero}, {self.bairro}, {self.cidade}, {self.estado}'



