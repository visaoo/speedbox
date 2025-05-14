from sqlalchemy import (Column, ForeignKey, Integer, select)
from sqlalchemy.orm import relationship, Session
from addressBase import AddressBase

class AddressEnterprise(AddressBase):
    __tablename__ = 'address_enterprise'
    
    _id_enterprise = Column(Integer, ForeignKey('enterprise.id'))
    
    enterprise = relationship('Enterprise', back_populates='address_enterprise')
    
    
def create_address_client(db: Session, enterprise_or_id, **kwargs) -> AddressEnterprise:
    #dps do visão criar o cliente, trocar os ... por client 
    
    if isinstance(enterprise_or_id, int):
        enterprise = db.query(...).filter_by(id=enterprise_or_id).first()
        if not enterprise:
            raise ValueError("Cliente não encontrado.")
    else:
        enterprise = enterprise_or_id

    address = AddressEnterprise(enterprise=enterprise, **kwargs)
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


def get_address_client(db:Session, address_id):
    stmt = select(AddressEnterprise).where(AddressEnterprise.id == address_id)
    return db.execute(stmt).scalars().first()

def get_address_by_client(db:Session, client_id):
    stmt = select(AddressEnterprise).where(AddressEnterprise._id_client == client_id)
    return db.execute(stmt).scalars().first()

def update_address_client(db:Session, address_id, address_data:dict):
    address = select(AddressEnterprise).where(AddressEnterprise.id == address_id)
    if address:
        for key, value in address_data.items():
            setattr(address, key, value)
        db.commit()
        db.refresh(address)
    return address

def delete_address_client(db: Session, address_id):
    address = select(AddressEnterprise).where(AddressEnterprise.id == address_id)
    if address:
        db.delete(address)
        db.commit
    return address