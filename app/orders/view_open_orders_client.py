from app.utils.get_connection import get_connection


def view_open_orders_client(client_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE client_id = ? AND status IN ('payment_pending', 'pending')", (client_id,))
        orders = cursor.fetchall()
    if not orders:
        print("Nenhum pedido em aberto.")
        return
    for order in orders:
        print(f"ID: {order[0]}, Total: {order[1]}, Data: {order[2]}, Descrição: {order[3]}, Status: {order[4]}, Origem: {order[5]}, Destino: {order[6]}")
