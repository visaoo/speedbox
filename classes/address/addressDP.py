from sqlalchemy import (Column, ForeignKey, Integer, select)
from sqlalchemy.orm import relationship, Session

from addressBase import AddressBase

class AddressDP(AddressBase):
    __tablename__ = 'address_delivery_person'
    
    _id_delivery_person = Column(Integer, ForeignKey('delivery_person.id'))
    
    delivery_person = relationship('DeliveryPerson', back_populates='address_delivery_person')

def create_address_delivery_person(db: Session, delivery_person_or_id, **kwargs) -> AddressDP:
    # dps do visão criar o delivery_person, trocar os ... por delivery person 
    
    if isinstance(delivery_person_or_id, int):
        delivery_person = db.query(...).filter_by(id=delivery_person_or_id).first()
        if not delivery_person:
            raise ValueError("Cliente não encontrado.")
    else:
        delivery_person = delivery_person_or_id

    address = AddressDP(delivery_person=delivery_person, **kwargs)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_address_client(db:Session, address_id):
    stmt = select(AddressDP).where(AddressDP.id == address_id)
    return db.execute(stmt).scalars().first()

def get_address_by_client(db:Session, delivery_person_id):
    stmt = select(AddressDP).where(AddressDP._id_client == delivery_person_id)
    return db.execute(stmt).scalars().first()

def update_address_client(db:Session, address_id, address_data:dict):
    address = select(AddressDP).where(AddressDP.id == address_id)
    if address:
        for key, value in address_data.items():
            setattr(address, key, value)
        db.commit()
        db.refresh(address)
    return address

def delete_address_client(db: Session, address_id):
    address = select(AddressDP).where(AddressDP.id == address_id)
    if address:
        db.delete(address)
        db.commit
    return address