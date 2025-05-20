from classes.resources import *
from app.orders.view_orders import view_orders

def delivery_person_dashboard(username):
    """
    Exibe o dashboard do entregador, permitindo que ele visualize as entregas disponíveis.

    Args:
        username (str): O nome de usuário do entregador logado.
    """
    
    # adicionar Visualizar pedido em aberto
    # Histórico de pedidos 
    while True:
        clear_screen()
        display_logo()
        print(f"\n{Colors.BOLD}DASHBOARD DO ENTREGADOR{Colors.ENDC} - Bem-vindo, {username}!")
        print(f"\n{Colors.YELLOW}1.{Colors.ENDC} Ver entregas disponíveis")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} Sair")
        
        choice = input(f"\n{Colors.GREEN}Escolha uma opção: {Colors.ENDC}")
        
        if choice == "1":
            view_orders("entregador")
        elif choice == "2":
            break