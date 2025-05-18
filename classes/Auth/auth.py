from auth_service import AuthService
from user.user import User


class Authenticator:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.auth_service.validate_credentials(username, password)
        return user

    def register(self, username: str, email: str, password: str) -> bool:
        return self.auth_service.register_user(username, email, password)

    def logout(self) -> bool:
        if not self.is_authenticated():
            return False
        self.auth_service.logout()
        return True

    def is_authenticated(self) -> bool:
        return self.auth_service.is_authenticated()
