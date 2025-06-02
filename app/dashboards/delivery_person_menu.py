from app.orders.accept_order_delivery_person import (
    accept_order_delivery_person,
)
from app.orders.update_order_status_delivery_person import (
    update_order_status_delivery_person,
)
from app.orders.view_orders_delivery_person import view_orders_delivery_person
from classes.resources import *


def delivery_person_menu(delivery_person_id):
    while True:
        clear_screen()
        display_logo()
        print(f"\n{Colors.BOLD}DASHBOARD DO ENTREGADOR{Colors.ENDC}")
        print(f"\n{Colors.YELLOW}1.{Colors.ENDC} Visualizar pedidos disponíveis")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} Aceitar um pedido")
        print(f"{Colors.YELLOW}3.{Colors.ENDC} Alterar status de um pedido")
        print(f"{Colors.YELLOW}4.{Colors.ENDC} Sair")

        choice = input(f"\n{Colors.GREEN}Escolha uma opção: {Colors.ENDC}").strip()
        if choice == "1":
            view_orders_delivery_person(delivery_person_id)
        elif choice == "2":
            accept_order_delivery_person(delivery_person_id)
        elif choice == "3":
            update_order_status_delivery_person(delivery_person_id)
        elif choice == "4":
            break
        else:
            print("Opção inválida!")
