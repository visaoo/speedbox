import sqlite3

def insert_boleto(due_date, typeline, transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO boleto (due_date, typeline, transaction_id)
            VALUES (?, ?, ?);
        """, (due_date, typeline, transaction_id))
        conn.commit()

def get_boleto_by_transaction(transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM boleto WHERE transaction_id = ?;", (transaction_id,))
        return cursor.fetchone()

def delete_boleto_by_transaction(transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM boleto WHERE transaction_id = ?;", (transaction_id,))
        conn.commit()
