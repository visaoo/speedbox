from app.dashboards.client_menu import client_menu
from app.dashboards.delivery_person_menu import delivery_person_menu
from app.dashboards.enterprise_menu import enterprise_menu
from app.login.login import login
from app.register.register_user import register_user
from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService
from classes.resources import *


# Menu principal
def main():
    authenticator = Authenticator(AuthService(db_path="speedbox.db"))
    while True:
        welcome_message()

        choice = main_menu()
        if choice == "1":
            user_id, user_type = login()
            if user_id:
                # Obter o ID correto com base no tipo de usuário
                    if user_type == "client":
                        client_menu(user_id)
                    elif user_type == "delivery_person":
                        delivery_person_menu(user_id)
                    elif user_type == "enterprise":
                        enterprise_menu(user_id)

        elif choice == "2":
            register_user("client")
        elif choice == "3":
            register_user("delivery_person")
        elif choice == "4":
            register_user("enterprise")
        elif choice == "5":
            print(f"{Colors.YELLOW}Saindo...{Colors.YELLOW}")
            break
        else:
            print(f"{Colors.RED}Opção inválida!{Colors.RED}")
            input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")


if __name__ == "__main__":
    main()
