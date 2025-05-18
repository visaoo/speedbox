class User:
    def __init__(
        self, username: str, email: str, senha: str, user_type: str = "client"
    ) -> None:
        """
        Inicializa um objeto User com as informações fornecidas.
        :param username: Nome de usuário
        :param email: Email do usuário
        :param senha: Senha do usuário
        :param user_type: Tipo de usuário (ex: cliente, entregador, empresa)
        """
        if not isinstance(username, str) or not username:
            raise ValueError("Username must be a non-empty string.")
        if not isinstance(email, str) or not email:
            raise ValueError("Email must be a non-empty string.")
        if not isinstance(senha, str) or not senha:
            raise ValueError("Password must be a non-empty string.")
        if not isinstance(user_type, str) or not user_type:
            raise ValueError("User type must be a non-empty string.")
        if user_type not in ["client", "delivery_person", "enterprise"]:
            raise ValueError(
                "User type must be one of: client, delivery_person, enterprise."
            )

        self._username = username
        self._email = email
        self._senha = senha
        self._user_type = user_type

    @property
    def username(self) -> str:
        """
        Retorna o nome de usuário.
        :return: Nome de usuário
        """
        return self._username

    @username.setter
    def username(self, value) -> None:
        """
        Define o nome de usuário.
        :param value: Novo nome de usuário
        """
        self._username = value

    @property
    def email(self) -> str:
        """
        Retorna o email do usuário.
        :return: Email do usuário
        """
        return self._email

    @email.setter
    def email(self, value) -> None:
        """
        Define o email do usuário.
        :param value: Novo email do usuário
        """
        self._email = value

    @property
    def senha(self) -> str:
        """
        Retorna a senha do usuário.
        :return: Senha do usuário
        """
        return self._senha

    @senha.setter
    def senha(self, value) -> None:
        """
        Define a senha do usuário.
        :param value: Nova senha do usuário
        """
        self._senha = value

    @property
    def user_type(self) -> str:
        """
        Retorna o tipo de usuário.
        :return: Tipo de usuário
        """
        return self._user_type

    @user_type.setter
    def user_type(self, value) -> None:
        """
        Define o tipo de usuário.
        :param value: Novo tipo de usuário
        """
        self._user_type = value

    def to_dict(self) -> dict:
        """
        Converte o objeto User em um dicionário JSON.
        :return: Dicionário representando o objeto User
        """
        return {
            "username": self.username,
            "email": self.email,
            "senha": self.senha,
            "user_type": self.user_type,
        }

    def __str__(self) -> str:
        """
        Retorna uma representação em string do objeto User.
        :return: Representação em string do objeto User
        """
        return f"User(username={self.username}, email={self.email})"
