from classes.resources import *
from app.orders.view_orders import view_orders

def enterprise_dashboard(username):
    """
    Exibe o dashboard da empresa, permitindo que ela visualize os pedidos recebidos.

    Args:
        username (str): O nome de usuário da empresa logada.
    """
    while True:
        clear_screen()
        display_logo()
        print(f"\n{Colors.BOLD}DASHBOARD DA EMPRESA{Colors.ENDC} - Bem-vindo, {username}!")
        print(f"\n{Colors.YELLOW}1.{Colors.ENDC} Ver pedidos recebidos")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} Sair")
        
        choice = input(f"\n{Colors.GREEN}Escolha uma opção: {Colors.ENDC}")
        
        if choice == "1":
            view_orders("empresa")
        elif choice == "2":
            break