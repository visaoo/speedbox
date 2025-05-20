from classes.resources import *
from validations.validations import get_input, none_word, is_email
from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService

auth = Authenticator(AuthService('database.db'))

def register_base_user(user_select):
    """
    Registra um novo usuário no sistema com base no tipo selecionado.

    Solicita nome de usuário, email e senha, e tenta registrar o usuário
    com o tipo correspondente (client, enterprise ou delivery_person).

    Args:
        user_select (str): A opção numérica que representa o tipo de usuário (ex: "1" para "client").

    Returns:
        dict or None: Um dicionário contendo 'username' e 'email' do usuário registrado
                      se o registro for bem-sucedido, caso contrário, retorna None.
    """
    username = get_input(f"{Colors.CYAN}Nome de usuário: {Colors.ENDC}", none_word)
    email = get_input(f"{Colors.CYAN}Email: {Colors.ENDC}", is_email)
    password = get_input(f"{Colors.CYAN}Senha: {Colors.ENDC}", none_word)
    
    user_types = {
        "1": "client",
        "2": "enterprise",
        "3": "delivery_person",
    }

    auth_response = auth.register(username, email, password, user_types[user_select])
    
    if auth_response:
        print(f"\n{Colors.GREEN}Usuário registrado com sucesso!{Colors.ENDC}")
        return {"username": username, "email": email}
    else:
        print(f"{Colors.RED}Email ou senha inválidos. Tente novamente.{Colors.ENDC}")
        return register_base_user(user_select)  # chama novamente se der errado
