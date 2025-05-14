from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship
from db.database import Base

class AddressEnterprise(Base):
    __tablename__ = 'address_enterprise'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    _street = Column(String(100))
    _number = Column(Integer)
    _neighborhood = Column(String(50))
    _city = Column(String(25))
    _state = Column(String(20))
    _id_enterprise = Column(Integer, ForeignKey('enterprise.id'))
    
    client = relationship('Enterprise', back_populates='address_enterprise')
    
    
    def __str__(self):
        return f'{self.rua}, {self.numero}, {self.bairro}, {self.cidade}, {self.estado}'