from sqlalchemy import (Column, ForeignKey, Integer)
from sqlalchemy.orm import relationship
from addressBase import AddressBase


class AddressClient(AddressBase):
    
    __tablename__ = 'address_client'
    
    _id_client = Column(Integer, ForeignKey('client.id'))
    
    client = relationship('Client', back_populates='address_client')


# origem = Address('Rua Folha Dourada', '6', 'Jardim Miragaia', 'São Paulo', 'SP')
# destino = Address('Rua Olivio Segatto', '1017', 'Centro', 'Tupi Paulista', 'SP')


# print(origem, destino)

# ford = Vehicle('model', 'mark', 'str', Vehicle_type.CARRO)


# print(ford.calculate_distance(origem, destino))
