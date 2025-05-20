from app.utils.get_connection import get_connection

# Login
def login(authenticator):
    username = input("Digite o nome de usuário: ").strip()
    password = input("Digite a senha: ").strip()
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