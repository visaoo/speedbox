from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService
from validations.validations import get_input, none_word

auth_service = AuthService()
auth = Authenticator(auth_service)

def login() -> tuple[str | None, str | None]:
    """
    Função para realizar o login do usuário.
    Retorna o ID do usuário e o tipo de usuário se o login for bem-sucedido,
    ou None se o login falhar.
    :return: Tuple (user_id, user_type) ou (None, None) se falhar
    """
    username = get_input("Digite o nome de usuário: ", none_word).strip()
    password = get_input("Digite a senha: ", none_word).strip()

    user = auth.login(username, password)

    if isinstance(user, dict):
        return user.get("id"), user.get("user_type")
    else:
        print("Usuário ou senha inválidos!")
        return None, None
