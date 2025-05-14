from sqlalchemy import (Column, ForeignKey, Integer, String)
from sqlalchemy.orm import relationship
from db.database import Base




class AddressClient(Base):
    __tablename__ = 'address client'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    _street = Column(String(100))
    _number = Column(Integer)
    _neighborhood = Column(String(50))
    _city = Column(String(25))
    _state = Column(String(20))
    _id_client = Column(Integer, ForeignKey('client.id'))
    
    client = relationship('Client')
    
    
    def __str__(self):
        return f'{self.rua}, {self.numero}, {self.bairro}, {self.cidade}, {self.estado}'


# origem = Address('Rua Folha Dourada', '6', 'Jardim Miragaia', 'São Paulo', 'SP')
# destino = Address('Rua Olivio Segatto', '1017', 'Centro', 'Tupi Paulista', 'SP')


# print(origem, destino)

# ford = Vehicle('model', 'mark', 'str', Vehicle_type.CARRO)


# print(ford.calculate_distance(origem, destino))
