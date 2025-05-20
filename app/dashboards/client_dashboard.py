from classes.resources import *
from app.orders.create_new_order import create_new_order
from app.orders.view_orders import view_orders

def client_dashboard(username):
    """
    Exibe o dashboard do cliente, permitindo que ele faça novos pedidos ou visualize os existentes.

    Args:
        username (str): O nome de usuário do cliente logado.
    """
    while True:
        clear_screen()
        display_logo()
        print(f"\n{Colors.BOLD}DASHBOARD DO CLIENTE{Colors.ENDC} - Bem-vindo, {username}!")
        print(f"\n{Colors.YELLOW}1.{Colors.ENDC} Fazer novo pedido")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} Ver meus pedidos")
        print(f"{Colors.YELLOW}3.{Colors.ENDC} Sair")
        
        choice = input(f"\n{Colors.GREEN}Escolha uma opção: {Colors.ENDC}")
        
        if choice == "1":
            create_new_order()
        elif choice == "2":
            view_orders("cliente")
        elif choice == "3":
            break
