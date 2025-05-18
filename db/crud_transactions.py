import sqlite3

def insert_transaction(payment_method, status, order_client_id=None, order_enterprise_id=None):
    if bool(order_client_id) == bool(order_enterprise_id):
        raise ValueError("Informe apenas um ID de pedido (cliente OU empresa).")
    
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO transactions (payment_method, status, order_client_id, order_enterprise_id)
            VALUES (?, ?, ?, ?);
        """, (payment_method, status, order_client_id, order_enterprise_id))
        conn.commit()

def get_by_id(transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?;", (transaction_id,))
        return cursor.fetchone()

def update_status(transaction_id, status):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE transactions SET status = ? WHERE id = ?;", (status, transaction_id))
        conn.commit()

def delete(transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?;", (transaction_id,))
        conn.commit()
