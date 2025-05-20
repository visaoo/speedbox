from classes.order import Order

# Funcionalidades da Empresa
def view_order_history_enterprise(enterprise_id):
    orders = Order.get_by_enterprise(enterprise_id)
    if not orders:
        print("Nenhum pedido encontrado.")
        return
    for order in orders:
        print(f"ID: {order[0]}, Total: {order[1]}, Data: {order[2]}, Descrição: {order[3]}, Status: {order[4]}, Origem: {order[5]}, Destino: {order[6]}")