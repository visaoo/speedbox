from classes.address.address import Address
from classes.user.client import Client

a = Address(street='Rua A', city='São Paulo', state='SP', number='123', neighborhood='Centro')
c = Client(name='João', cpf='12345678901', phone='11987654321', birth_date='1990-01-01', address=a)

c.insert()
