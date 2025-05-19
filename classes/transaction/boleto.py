from dataclasses import dataclass
from random import randint
from datetime import datetime, timedelta

import sqlite3

@dataclass
class Boleto:
    def __init__(self):
        self.due_date = self.generate_due_date()
        self.typeline = self.generate_typeline()

    def generate_due_date(self):
        due_date =  datetime.now() + timedelta(days=3)
        return due_date.strftime("%d/%m/%Y")
    
    def generate_typeline():
        return ''.join(str(randint(0, 9)) for _ in range(47))
    

    def insert(due_date, typeline, transaction_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO boleto (due_date, typeline, transaction_id)
                VALUES (?, ?, ?);
            """, (due_date, typeline, transaction_id))
            conn.commit()

    def get_by_transaction(transaction_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM boleto WHERE transaction_id = ?;", (transaction_id,))
            return cursor.fetchone()

    def delete_by_transaction(transaction_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM boleto WHERE transaction_id = ?;", (transaction_id,))
            conn.commit()

        
    
    
    def to_dict(self):
        return {
            "due_date": self.due_date,
            "typeline": self.typeline
        }
    
    def __str__(self):
        return f"Boleto(due_date={self.due_date}, typeline={self.typeline})"