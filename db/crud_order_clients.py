import sqlite3

STATUS_VALUES = ('payment_pending', 'pending', 'completed', 'canceled')

def insert(total, date, client_id, delivery_person_id, addrss_final, addrss_initial, description, status='pending'):
    if status not in STATUS_VALUES:
        raise ValueError("Status inválido.")
    
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO orders (total, date, client_id, delivery_person_id, addrss_final, addrss_initial, description,status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """, (total, date, client_id, delivery_person_id, addrss_final, addrss_initial, description, status))
        conn.commit()

def get_by_client(client_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE client_id = ?;", (client_id,))
        return cursor.fetchall()

def update_delivery_person(order_id, delivery_person_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE orders SET delivery_person_id = ? WHERE id = ?;", (delivery_person_id, order_id))
        conn.commit()

def update_status(order_id, new_status):
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
