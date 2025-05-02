class User:
    def __init__(self, username: str, email: str, senha: str):
        self._username = username
        self._email = email
        self._senha = senha

    @property
    def username(self):
        return self._username

    @username.setter
    def login(self, value):
        self._username = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def senha(self):
        return self._senha

    @senha.setter
    def senha(self, value):
        self._senha = value