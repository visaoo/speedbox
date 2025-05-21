from classes.resources import *

from validations.validations import get_input, none_word

from app.orders.view_order_history_client import view_order_history_client
from app.orders.make_order_client import make_order_client
from app.orders.view_open_orders_client import view_open_orders_client


def client_menu(client_id):
    while True:
        clear_screen()
        display_logo()
        print(f"\n{Colors.BOLD}DASHBOARD DO CLIENTE{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}1.{Colors.ENDC} Visualizar histórico de pedidos")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} Fazer um pedido")
        print(f"{Colors.YELLOW}3.{Colors.ENDC} Ver pedidos em aberto")
        print(f"{Colors.YELLOW}4.{Colors.ENDC} Sair")
        
        choice = get_input(f"{Colors.GREEN}Escolha uma opção: {Colors.ENDC}", none_word).strip()
        if choice == "1":
            view_order_history_client(client_id)
        elif choice == "2":
            make_order_client(client_id)
        elif choice == "3":
            view_open_orders_client(client_id)
        elif choice == "4":
            break
        else:
            print(f"\n{Colors.RED}Opção inválida!{Colors.RED}")
            input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")