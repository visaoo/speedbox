import sqlite3

def insert(name, cpf, birth_date, celphone,user_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO delivery_person (name, cpf, birth_date, celphone, user_id)
            VALUES (?, ?, ?, ?, ?);
        """, (name, cpf, birth_date, celphone, user_id))
        conn.commit()

def get_all():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM delivery_person;")
        return cursor.fetchall()

def get_by_id(person_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM delivery_person WHERE id = ?;", (person_id,))
        return cursor.fetchone()

def update(person_id, name=None, cpf=None, user_id=None, birth_date=None, celphone=None):
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
        if birth_date:  
            fields.append("birth_date = ?")
            values.append(birth_date)
        if celphone:
            fields.append("celphone = ?")
            values.append(celphone)
        if not fields:
            return

        values.append(person_id)
        query = f"UPDATE delivery_person SET {', '.join(fields)} WHERE id = ?;"
        cursor.execute(query, values)
        conn.commit()

def delete(person_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM delivery_person WHERE id = ?;", (person_id,))
        conn.commit()
