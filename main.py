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
        print("\n=== Sistema de Delivery ===")
        print("1. Login")
        print("2. Cadastrar Cliente")
        print("3. Cadastrar Entregador")
        print("4. Cadastrar Empresa")
        print("5. Sair")
        choice = input("Escolha uma opção: ").strip()
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
                            print("Erro: Cliente não encontrado.")
                    elif user_type == "delivery_person":
                        cursor.execute("SELECT id FROM delivery_person WHERE user_id = ?", (user_id,))
                        entity_id = cursor.fetchone()
                        if entity_id:
                            delivery_person_menu(entity_id[0])
                        else:
                            print("Erro: Entregador não encontrado.")
                    elif user_type == "enterprise":
                        cursor.execute("SELECT id FROM enterprises WHERE user_id = ?", (user_id,))
                        entity_id = cursor.fetchone()
                        if entity_id:
                            enterprise_menu(entity_id[0])
                        else:
                            print("Erro: Empresa não encontrado.")
        elif choice == "2":
            register_user(authenticator, "client")
        elif choice == "3":
            register_user(authenticator, "delivery_person")
        elif choice == "4":
            register_user(authenticator, "enterprise")
        elif choice == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()