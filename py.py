
from classes.user.client import Client
from validations.validations import *

# name = get_input("Digite seu nome: ", none_word)
# cpf = get_input("Digite seu CPF: ", none_word)
# phone = get_input("Digite seu telefone: ", none_word)
# birthday = get_input("Digite sua data de nascimento (YYYY-MM-DD): ", none_word)
# address = Address(
#     street=get_input("Digite seu endereço: ", none_word),
#     number=get_input("Digite o número da sua casa: ", none_word),
#     neighborhood=get_input("Digite seu bairro: ", none_word),
#     city=get_input("Digite sua cidade: ", none_word),
#     state=get_input("Digite seu estado: ", none_word)
# )
# user_id = 1

# cliente = Client(
#     name=name,
#     cpf=cpf,
#     phone=phone,
#     birth_date=birthday,
#     address=address,
#     user_id=user_id
# )

# # print(cliente)

# cliente.insert()
# a = Client.get_all()
# print(a)


a = Client.get_by_id(1)

# Filtro de USER ID
