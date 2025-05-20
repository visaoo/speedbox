from app.orders.view_orders_delivery_person import view_orders_delivery_person
from app.orders.accept_order_delivery_person import accept_order_delivery_person
from app.orders.update_order_status_delivery_person import update_order_status_delivery_person

def delivery_person_menu(delivery_person_id):
    while True:
        print("\n=== Menu do Entregador ===")
        print("1. Visualizar pedidos disponíveis")
        print("2. Aceitar um pedido")
        print("3. Alterar status de um pedido")
        print("4. Sair")
        choice = input("Escolha uma opção: ").strip()
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