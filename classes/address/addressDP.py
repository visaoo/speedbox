from sqlalchemy import (Column, ForeignKey, Integer)
from sqlalchemy.orm import relationship

from addressBase import AddressBase

class AddressDP(AddressBase):
    __tablename__ = 'address_delivery_person'
    
    _id_delivery_person = Column(Integer, ForeignKey('delivery_person.id'))
    
    delivery_person = relationship('DeliveryPerson', back_populates='address_delivery_person')

