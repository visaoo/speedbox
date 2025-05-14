from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text)
from sqlalchemy.orm import relationship

from db.database import Base

class AddressDP(Base):
    __tablename__ = 'address_delivery_person'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    _street = Column(String(100))
    _number = Column(Integer)
    _neighborhood = Column(String(50))
    _city = Column(String(25))
    _state = Column(String(20))
    _id_delivery_person = Column(Integer, ForeignKey('delivery_person.id'))
    
    delivery_person = relationship('DeliveryPerson', back_populates='address_delivery_person')
    
    
    def __str__(self):
        return f'{self.rua}, {self.numero}, {self.bairro}, {self.cidade}, {self.estado}'

