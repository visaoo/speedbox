import sqlite3

def insert_enterprise(name, cnpj, user_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO enterprises (name, cnpj, user_id)
            VALUES (?, ?, ?);
        """, (name, cnpj, user_id))
        conn.commit()

def get_all_enterprises():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM enterprises;")
        return cursor.fetchall()

def get_enterprise_by_id(enterprise_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM enterprises WHERE id = ?;", (enterprise_id,))
        return cursor.fetchone()

def update_enterprise(enterprise_id, name=None, cnpj=None, user_id=None):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        fields, values = [], []

        if name:
            fields.append("name = ?")
            values.append(name)
        if cnpj:
            fields.append("cnpj = ?")
            values.append(cnpj)
        if user_id:
            fields.append("user_id = ?")
            values.append(user_id)

        if not fields:
            return

        values.append(enterprise_id)
        query = f"UPDATE enterprises SET {', '.join(fields)} WHERE id = ?;"
        cursor.execute(query, values)
        conn.commit()

def delete_enterprise(enterprise_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM enterprises WHERE id = ?;", (enterprise_id,))
        conn.commit()
