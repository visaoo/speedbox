import sqlite3

def insert(key, transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pix (key, transaction_id)
            VALUES (?, ?);
        """, (key, transaction_id))
        conn.commit()

def get_by_transaction(transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pix WHERE transaction_id = ?;", (transaction_id,))
        return cursor.fetchone()

def delete_by_transaction(transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pix WHERE transaction_id = ?;", (transaction_id,))
        conn.commit()
