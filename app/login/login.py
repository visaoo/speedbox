from validations.validations import get_input, none_word

from app.utils.get_connection import get_connection


def login(authenticator):
    username = get_input("Digite o nome de usuário: ", none_word).strip()
    password = get_input("Digite a senha: ", none_word).strip()
    user = authenticator.authenticate(username, password)
    if user:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_type FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                return result[0], result[1]
    print("Usuário ou senha inválidos!")
    return None, None