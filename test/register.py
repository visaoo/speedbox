from classes.Auth.auth import Authenticator, EnumUserType
from classes.Auth.auth_service import AuthService
from classes.user.client import Client
from classes.address.address import Address
from validations.validations import get_input, is_email, none_word

auth = Authenticator(AuthService("database.db"))

for i in range(1):
    username = get_input("Insira seu username: ", none_word)
    email = get_input("Insira seu email: ", is_email)
    password = get_input("Insira sua password: ", none_word)
    user_type = EnumUserType(
        get_input(
            "Insira seu tipo de usuário (client, delevery_person e enterprise): ",
            none_word,
        ).strip()
    )
    auth_response = auth.register(username, email, password, user_type)

    if auth_response:
        print(auth_response)
        break
    else:
        print("Email ou senha inválidos. Tente novamente.")
