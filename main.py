from app.dashboards.client_menu import client_menu
from app.dashboards.delivery_person_menu import delivery_person_menu
from app.dashboards.enterprise_menu import enterprise_menu
from app.login.login import login
from app.register.register_user import register_user
from classes.Auth.auth import EnumUserType
from classes.resources import *
from db.database import get_connection

# Menu principal
def main() -> None:
    """
    Função principal que executa o menu do sistema de delivery.
    Esta função exibe o menu principal, permite que o usuário faça login ou se registre,
    e direciona o usuário para o menu apropriado com base no tipo de usuário.
    Além disso, verifica a conexão com o banco de dados antes de prosseguir.
    :return: None
    """
    while True:
        # Verificando se o banco de dados está funcional
        if not check_database_connection():
            continue

        welcome_message()

        choice = main_menu()
        if choice == "1":
            user_id, user_type = login()
            
            if user_id:
                if user_type == EnumUserType.CLIENT.value:
                    client_menu(user_id)
                elif user_type == EnumUserType.DELIVERY_PERSON.value:
                    delivery_person_menu(user_id)
                elif user_type == EnumUserType.ENTERPRISE.value:
                    enterprise_menu(user_id)
            else:
                print(f"{Colors.RED}Erro ao fazer login!{Colors.RED}")
                input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
        elif choice == "2":
            register_user(EnumUserType.CLIENT.value)
        elif choice == "3":
            register_user(EnumUserType.DELIVERY_PERSON.value)
        elif choice == "4":
            register_user(EnumUserType.ENTERPRISE.value)
        elif choice == "5":
            print(f"{Colors.YELLOW}Saindo...{Colors.YELLOW}")
            break
        else:
            print(f"{Colors.RED}Opção inválida!{Colors.RED}")
            input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")

def check_database_connection():
    conn = get_connection()
    if conn is None:
        print(f"{Colors.RED}Erro ao conectar ao banco de dados!{Colors.RED}")
        input(f"\n{Colors.YELLOW}Pressione Enter para sair...{Colors.ENDC}")
        return


if __name__ == "__main__":
    main()
