from classes.resources import *
from validations.validations import get_input, none_word
from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService

auth = Authenticator(AuthService('database.db'))

from app.dashboards.client_dashboard import client_dashboard
from app.dashboards.enterprise_dashboard import enterprise_dashboard
from app.dashboards.delivery_person_dashboard import delivery_person_dashboard

def login():
    """
    Realiza o processo de login do usuário, autenticando as credenciais
    e redirecionando para o dashboard apropriado com base no tipo de usuário.
    """
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}LOGIN{Colors.ENDC}")
    
    username = get_input(f"{Colors.CYAN}Nome de usuário: {Colors.ENDC}", none_word)
    password = get_input(f"{Colors.CYAN}Senha: {Colors.ENDC}", none_word)

    user_login = auth.login(username, password)
    if user_login:
        print(f"\n{Colors.GREEN}Login realizado com sucesso!{Colors.ENDC}")
        time.sleep(1)

        # remover simualação e adiconar entrada pelo tipo direto em breve
        user_type = input(f"\n{Colors.CYAN}Simular tipo de usuário (1-Cliente, 2-Empresa, 3-Entregador): {Colors.ENDC}")

        if user_type == "1":
            client_dashboard(username)
        elif user_type == "2":
            enterprise_dashboard(username)
        elif user_type == "3":
            delivery_person_dashboard(username)
    else:
        print(f"\n{Colors.RED}Falha no login. Verifique suas credenciais.{Colors.ENDC}")
        input(f"{Colors.YELLOW}Pressione Enter para tentar novamente...{Colors.ENDC}")
