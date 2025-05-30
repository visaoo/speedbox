from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService
from validations.validations import get_input, none_word

auth_service = AuthService()
auth = Authenticator(auth_service)


def login():
    username = get_input("Digite o nome de usuário: ", none_word).strip()
    password = get_input("Digite a senha: ", none_word).strip()

    user = auth.login(username, password)

    if isinstance(user, dict):
        return user.get("id"), user.get("user_type")
    else:
        print("Usuário ou senha inválidos!")
        return None, None
