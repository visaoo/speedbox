import hashlib
import sqlite3

from classes.user.user import User
from db.database import get_connection

class AuthService:
    def __init__(self, db_path='speedbox.db') -> None:
        """
        Inicializa o serviço de autenticação com o caminho do banco de dados.
        param db_path: Caminho do banco de dados SQLite.
        """
        self.db_path = db_path
        self.current_user = None

    def _hash_password(self, password: str) -> str:
        """
        Retorna o hash da senha usando SHA-256.
        param password: Senha a ser hashada
        return: O hash da senha.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_credentials(self, username: str, password: str) -> User | None:
        """
        Valida as credenciais do usuário no banco de dados. 
        param username: Nome de usuário
        param password: Senha do usuário
        return: Um objeto User se as credenciais forem válidas, None caso contrário.
        """
        hashed = self._hash_password(password)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, email, password, id, user_type FROM users WHERE username = ? AND password = ?",
                (username, hashed),
            )
            row = cursor.fetchone()
            if row:
                # print(f"Usuário encontrado: {row}")
                user = User(*row)  # usando destructuring
                self.current_user = user
                return user
        return None

    def logout(self) -> None:
        """
        Realiza o logout do usuário atual."""
        self.current_user = None

    def is_authenticated(self) -> bool:
        """
        Verifica se o usuário está autenticado.
        return: True se o usuário estiver autenticado, False caso contrário.
        """
        return self.current_user is not None

    def register_user(self, username: str, email: str, password: str, user_type) -> bool:
        """
        Registra um novo usuário no banco de dados.
        param username: Nome de usuário
        param email: Email do usuário
        param password: Senha do usuário
        param user_type: Tipo de usuário (ex: client, delivery_person, enterprise)
        return: True se o registro for bem-sucedido, False caso contrário.
        """
        # user_type = user_type.value
        hashed = self._hash_password(password)
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    'INSERT INTO users (username, email, password, user_type) VALUES (?, ?, ?, ?)',
                    (username, email, hashed, user_type)
                )
                conn.commit()

                # user = User(username, email, hashed, user_type)

                return True
            except sqlite3.IntegrityError:
                return False

    def find_user_by_id(self, user_id: int) -> User | None:
        """
        Encontra um usuário pelo ID.
        param user_id: ID do usuário
        return: Faz uma requisicao no banco de dados e retorna um objeto User se o usuário for encontrado, None caso contrário.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, email, password, id FROM users WHERE id = ?",
                (user_id,),
            )
            row = cursor.fetchone()
            if row:
                return User(*row)
        return None
    
    def find_user_by_username(self, username: str) -> User | None:
        """
        Encontra um usuário pelo nome de usuário.
        param username: Nome de usuário
        return: Faz uma requisicao no banco de dados e retorna um objeto User se o usuário for encontrado, None caso contrário.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT username, email, password, id FROM users WHERE username = ?",
                (username,),
            )
            row = cursor.fetchone()
            if row:
                return User(*row)
        return None

    def is_user_registered(self, username: str, email) -> bool:
        """
        Verifica se um usuário já existe no banco de dados.
        param username: Nome de usuário
        param email: Email do usuário
        return: True se o usuário existir, False caso contrário.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id FROM users WHERE username = ? OR email = ?",
                (username, email),
            )
            return cursor.fetchone() is not None
