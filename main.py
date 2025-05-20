import time
from classes.resources import *

from app.register.register_client import register_client
from app.register.register_enterprise import register_enterprise
from app.register.register_delivery_person import register_delivery_person
from app.register.register_menu import register_menu
from app.login.login import login


def main():
    """
    Função principal do aplicativo SpeedBox.

    Exibe uma mensagem de boas-vindas e entra em um loop para apresentar o menu principal,
    permitindo que o usuário escolha entre fazer login, registrar um novo usuário
    (cliente, empresa ou entregador) ou sair do aplicativo.
    """
    welcome_message()
    
    while True:
        choice = main_menu()
        # Login
        if choice == "1":
            login()
        # Register
        elif choice == "2":
            register_choice = register_menu()
            if register_choice == "1":
                register_client()
            elif register_choice == "2":
                register_enterprise()
            elif register_choice == "3":
                register_delivery_person()
        #Exit
        elif choice == "3":
            clear_screen()
            display_logo()
            print(f"\n{Colors.GREEN}Obrigado por usar o SpeedBox! Até logo!{Colors.ENDC}")
            time.sleep(1.5)
            clear_screen()
            break

if __name__ == "__main__":
    main()
