from validations.validations import get_input, none_word
from app.utils.get_connection import get_connection
from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService

auth = Authenticator(AuthService(db_path="database.db"))

def login():
    username = get_input("Digite o nome de usuário: ", none_word).strip()
    password = get_input("Digite a senha: ", none_word).strip()

    user = auth.login(username, password)

    if isinstance(user, dict):
        return user.get("id"), user.get("user_type")
    else:
        print("Usuário ou senha inválidos!")
        return None, None