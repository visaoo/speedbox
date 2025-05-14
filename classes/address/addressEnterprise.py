from sqlalchemy import (Column, ForeignKey, Integer)
from sqlalchemy.orm import relationship
from addressBase import AddressBase

class AddressEnterprise(AddressBase):
    __tablename__ = 'address_enterprise'
    
    _id_enterprise = Column(Integer, ForeignKey('enterprise.id'))
    
    enterprise = relationship('Enterprise', back_populates='address_enterprise')