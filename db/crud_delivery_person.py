import sqlite3

def insert_delivery_person(name, cpf, user_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO delivery_person (name, cpf, user_id)
            VALUES (?, ?, ?);
        """, (name, cpf, user_id))
        conn.commit()

def get_all_delivery_persons():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM delivery_person;")
        return cursor.fetchall()

def get_delivery_person_by_id(person_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM delivery_person WHERE id = ?;", (person_id,))
        return cursor.fetchone()

def update_delivery_person(person_id, name=None, cpf=None, user_id=None):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        fields, values = [], []

        if name:
            fields.append("name = ?")
            values.append(name)
        if cpf:
            fields.append("cpf = ?")
            values.append(cpf)
        if user_id:
            fields.append("user_id = ?")
            values.append(user_id)

        if not fields:
            return

        values.append(person_id)
        query = f"UPDATE delivery_person SET {', '.join(fields)} WHERE id = ?;"
        cursor.execute(query, values)
        conn.commit()

def delete_delivery_person(person_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM delivery_person WHERE id = ?;", (person_id,))
        conn.commit()
