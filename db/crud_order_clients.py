import sqlite3

STATUS_VALUES = ('payment_pending', 'pending', 'completed', 'canceled')

def insert_order_client(total, date, client_id, delivery_person_id, addrss_final, addrss_initial, status='pending'):
    if status not in STATUS_VALUES:
        raise ValueError("Status inválido.")
    
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (total, date, client_id, delivery_person_id, addrss_final, addrss_initial, status)
            VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (total, date, client_id, delivery_person_id, addrss_final, addrss_initial, status))
        conn.commit()

def get_orders_by_client(client_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE client_id = ?;", (client_id,))
        return cursor.fetchall()

def update_order_status(order_id, new_status):
    if new_status not in STATUS_VALUES:
        raise ValueError("Status inválido.")
    
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET status = ? WHERE id = ?;", (new_status, order_id))
        conn.commit()

def delete_order(order_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orders WHERE id = ?;", (order_id,))
        conn.commit()
