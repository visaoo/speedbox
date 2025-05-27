from app.orders.make_order_enterprise import make_order_enterprise
from app.orders.view_open_orders_enterprise import view_open_orders_enterprise
from app.orders.view_order_history_enterprise import (
    view_order_history_enterprise,
)
from classes.resources import *
from validations.validations import get_input, none_word


def enterprise_menu(enterprise_id):
    while True:
        print(f"\n{Colors.BOLD}DASHBOARD DA EMPRESA{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}1.{Colors.ENDC} Visualizar histórico de pedidos")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} Fazer um pedido")
        print(f"{Colors.YELLOW}3.{Colors.ENDC} Ver pedidos em aberto")
        print(f"{Colors.YELLOW}4.{Colors.ENDC} Sair")
        choice = get_input(f"{Colors.GREEN}Escolha uma opção: {Colors.ENDC}", none_word).strip()
        if choice == "1":
            view_order_history_enterprise(enterprise_id)
        elif choice == "2":
            make_order_enterprise(enterprise_id)
        elif choice == "3":
            view_open_orders_enterprise(enterprise_id)
        elif choice == "4":
            break
        else:
            print(f"\n{Colors.RED}Opção inválida!{Colors.RED}")
            input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
