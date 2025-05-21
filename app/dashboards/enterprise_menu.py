from validations.validations import get_input, none_word

from app.orders.view_order_history_enterprise import view_order_history_enterprise
from app.orders.make_order_enterprise import make_order_enterprise
from app.orders.view_open_orders_enterprise import view_open_orders_enterprise


def enterprise_menu(enterprise_id):
    while True:
        print("\n=== Menu da Empresa ===")
        print("1. Visualizar histórico de pedidos")
        print("2. Fazer um pedido")
        print("3. Ver pedidos em aberto")
        print("4. Sair")
        choice = get_input("Escolha uma opção: ", none_word).strip()
        if choice == "1":
            view_order_history_enterprise(enterprise_id)
        elif choice == "2":
            make_order_enterprise(enterprise_id)
        elif choice == "3":
            view_open_orders_enterprise(enterprise_id)
        elif choice == "4":
            break
        else:
            print("Opção inválida!")
