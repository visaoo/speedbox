from sqlalchemy import (Column, ForeignKey, Integer, select)
from sqlalchemy.orm import relationship, Session
from addressBase import AddressBase




class AddressClient(AddressBase):
    
    __tablename__ = 'address_client'
    
    _id_client = Column(Integer, ForeignKey('client.id'))
    
    client = relationship('Client', back_populates='address_client')



def create_address_client(db: Session, client_or_id, **kwargs) -> AddressClient:
    #dps do visão criar o cliente, trocar os ... por client 
    
    if isinstance(client_or_id, int):
        client = db.query(...).filter_by(id=client_or_id).first()
        if not client:
            raise ValueError("Cliente não encontrado.")
    else:
        client = client_or_id

    address = AddressClient(client=client, **kwargs)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_address_client(db:Session, address_id):
    stmt = select(AddressClient).where(AddressClient.id == address_id)
    return db.execute(stmt).scalars().first()

def get_address_by_client(db:Session, client_id):
    stmt = select(AddressClient).where(AddressClient._id_client == client_id)
    return db.execute(stmt).scalars().first()

def update_address_client(db:Session, address_id, address_data:dict):
    address = select(AddressClient).where(AddressClient.id == address_id)
    if address:
        for key, value in address_data.items():
            setattr(address, key, value)
        db.commit()
        db.refresh(address)
    return address

def delete_address_client(db: Session, address_id):
    address = select(AddressClient).where(AddressClient.id == address_id)
    if address:
        db.delete(address)
        db.commit
    return address