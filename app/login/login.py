from classes.resources import *

from validations.validations import get_input, none_word

from app.utils.get_connection import get_connection


def login(authenticator):
    username = get_input(f"{Colors.CYAN}Nome de usuário: {Colors.ENDC}", none_word).strip()
    password = get_input(f"{Colors.CYAN}Senha: {Colors.ENDC}", none_word).strip()
    user = authenticator.authenticate(username, password)
    if user:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_type FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                return result[0], result[1]
    print(f"\n{Colors.RED}Falha no login. Verifique suas credenciais.{Colors.ENDC}")
    input(f"{Colors.YELLOW}Pressione Enter para tentar novamente...{Colors.ENDC}")
    return None, None