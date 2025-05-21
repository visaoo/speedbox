from classes.resources import *

from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService

from app.utils.get_connection import get_connection
from app.login.login import login
from app.dashboards.client_menu import client_menu
from app.dashboards.enterprise_menu import enterprise_menu
from app.dashboards.delivery_person_menu import delivery_person_menu
from app.utils.get_connection import get_connection

from app.register.register_user import register_user

# Menu principal
def main():
    authenticator = Authenticator(AuthService(db_path="database.db"))
    while True:
        clear_screen()
        display_logo()
        welcome_message()

        choice = main_menu()
        if choice == "1":
            user_id, user_type = login(authenticator)
            if user_id:
                # Obter o ID correto com base no tipo de usuário
                with get_connection() as conn:
                    cursor = conn.cursor()
                    if user_type == "client":
                        cursor.execute("SELECT id FROM clients WHERE user_id = ?", (user_id,))
                        entity_id = cursor.fetchone()
                        if entity_id:
                            client_menu(entity_id[0])
                        else:
                            print(f"{Colors.RED}Erro: Cliente não encontrado.{Colors.RED}")
                    elif user_type == "delivery_person":
                        cursor.execute("SELECT id FROM delivery_person WHERE user_id = ?", (user_id,))
                        entity_id = cursor.fetchone()
                        if entity_id:
                            delivery_person_menu(entity_id[0])
                        else:
                            print(f"{Colors.RED}Erro: Entregador não encontrado.{Colors.RED}")
                            
                    elif user_type == "enterprise":
                        cursor.execute("SELECT id FROM enterprises WHERE user_id = ?", (user_id,))
                        entity_id = cursor.fetchone()
                        if entity_id:
                            enterprise_menu(entity_id[0])
                        else:
                            print(f"{Colors.RED}Erro: Empresa não encontrado.{Colors.RED}")
                            
        elif choice == "2":
            register_user(authenticator, "client")
        elif choice == "3":
            register_user(authenticator, "delivery_person")
        elif choice == "4":
            register_user(authenticator, "enterprise")
        elif choice == "5":
            print(f"{Colors.YELLOW}Saindo...{Colors.YELLOW}")
            break
        else:
            print(f"{Colors.RED}Opção inválida!{Colors.RED}")
            input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")

if __name__ == "__main__":
    main()
