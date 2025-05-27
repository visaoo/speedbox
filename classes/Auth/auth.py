from enum import Enum

from classes.Auth.auth_service import AuthService
from classes.user.user import User


class EnumUserType(Enum):
    """
    Enumeração para os tipos de usuário.
    """
    CLIENT = "client"
    DELIVERY_PERSON = "delivery_person"
    ENTERPRISE = "enterprise"


class Authenticator:
    def __init__(self, auth_service: AuthService) -> None:
        """
        Inicializa o autenticador com um serviço de autenticação.
        param auth_service: Instância do serviço de autenticação.
        """
        self.auth_service = auth_service

    def authenticate(self, username: str, password: str) -> User | None:
        """
        Autentica o usuário com as credenciais fornecidas.
        param username: Nome de usuário
        param password: Senha do usuário
        return: Um objeto User se as credenciais forem válidas, None caso contrário.
        """
        user = self.auth_service.validate_credentials(username, password)
        return user

    def register(
        self, username: str, email: str, password: str, user_type: EnumUserType
    ) -> bool:
        """
        Registra um novo usuário no banco de dados.
        param username: Nome de usuário
        param email: Email do usuário
        param password: Senha do usuário
        param user_type: Tipo de usuário (ex: client, delivery_person, enterprise)
        return: True se o registro for bem-sucedido, False caso contrário.
        """
        return self.auth_service.register_user(username, email, password, user_type)

    def login(self, username: str, password: str) -> bool | dict[str, str]:
        """
        Realiza o login do usuário com as credenciais fornecidas.
        param username: Nome de usuário
        param password: Senha do usuário
        return: Um dicionário com os dados do usuário se o login for bem-sucedido, False caso contrário.
        """
        if self.is_authenticated():
            return False
        user = self.authenticate(username, password)
        if user:
            return user.to_dict()
        return False

    def logout(self) -> bool:
        """
        Realiza o logout do usuário atual.
        return: True se o logout for bem-sucedido, False caso contrário.
        """
        if not self.is_authenticated():
            return False
        self.auth_service.logout()
        return True

    def is_authenticated(self) -> bool:
        """
        Verifica se o usuário está autenticado.
        return: True se o usuário estiver autenticado, False caso contrário.
        """
        return self.auth_service.is_authenticated()

    def find_user_id(self, id: int) -> User | None:
        """
        Encontra um usuário pelo ID.
        param id: ID do usuário
        return: Um objeto User se o ID for válido, None caso contrário.
        """
        return self.auth_service.find_user_by_id(id)

    def is_user_registered(self, username: str, email: str) -> bool:
        """
        Verifica se o usuário já está registrado.
        param username: Nome de usuário
        param email: Email do usuário
        return: True se o usuário já estiver registrado, False caso contrário.
        """
        return self.auth_service.is_user_registered(username, email)
