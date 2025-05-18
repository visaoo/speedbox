from classes.Auth.auth_service import AuthService
from classes.user.user import User

class Authenticator:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.auth_service.validate_credentials(username, password)
        return user

    def register(self, username: str, email: str, password: str) -> bool:
        return self.auth_service.register_user(username, email, password)
    
    def login (self, username: str, password: str) -> bool:
        if self.is_authenticated():
            return False
        user = self.authenticate(username, password)
        if user:
            return True
        return False

    def logout(self) -> bool:
        if not self.is_authenticated():
            return False
        self.auth_service.logout()
        return True

    def is_authenticated(self) -> bool:
        return self.auth_service.is_authenticated()