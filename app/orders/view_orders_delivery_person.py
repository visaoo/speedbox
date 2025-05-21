from app.utils.get_connection import get_connection


def view_orders_delivery_person(delivery_person_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE delivery_person_id = ? OR (status = 'pending' AND delivery_person_id IS NULL)", (delivery_person_id,))
        client_orders = cursor.fetchall()
        cursor.execute("SELECT * FROM orders_enterprises WHERE delivery_person_id = ? OR (status = 'pending' AND delivery_person_id IS NULL)", (delivery_person_id,))
        enterprise_orders = cursor.fetchall()
    
    if not (client_orders or enterprise_orders):
        print("Nenhum pedido disponível.")
        return
    print("\nPedidos de Clientes:")
    for order in client_orders:
        print(f"ID: {order[0]}, Total: {order[1]}, Data: {order[2]}, Descrição: {order[3]}, Status: {order[4]}, Origem: {order[5]}, Destino: {order[6]}")
    print("\nPedidos de Empresas:")
    for order in enterprise_orders:
        print(f"ID: {order[0]}, Total: {order[1]}, Data: {order[2]}, Descrição: {order[3]}, Status: {order[4]}, Origem: {order[5]}, Destino: {order[6]}")
