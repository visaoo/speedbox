from app.orders.view_order_history_client import view_order_history_client
from app.orders.make_order_client import make_order_client
from app.orders.view_open_orders_client import view_open_orders_client

# Menus
def client_menu(client_id):
    while True:
        print("\n=== Menu do Cliente ===")
        print("1. Visualizar histórico de pedidos")
        print("2. Fazer um pedido")
        print("3. Ver pedidos em aberto")
        print("4. Sair")
        choice = input("Escolha uma opção: ").strip()
        if choice == "1":
            view_order_history_client(client_id)
        elif choice == "2":
            make_order_client(client_id)
        elif choice == "3":
            view_open_orders_client(client_id)
        elif choice == "4":
            break
        else:
            print("Opção inválida!")
