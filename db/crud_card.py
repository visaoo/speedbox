import sqlite3

def insert_card(name, number, validity, cvc, flag, transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO card (name, number, validity, cvc, flag, transaction_id)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (name, number, validity, cvc, flag, transaction_id))
        conn.commit()

def get_card_by_transaction(transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM card WHERE transaction_id = ?;", (transaction_id,))
        return cursor.fetchone()

def delete_card_by_transaction(transaction_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM card WHERE transaction_id = ?;", (transaction_id,))
        conn.commit()
