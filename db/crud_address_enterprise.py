import sqlite3

def insert(street, city, state, enterprise_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO addresses_enterprises (street, city, state, enterprise_id)
            VALUES (?, ?, ?, ?);
        """, (street, city, state, enterprise_id))
        conn.commit()

def get_all():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM addresses_enterprises;")
        return cursor.fetchall()

def get_by_id(address_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM addresses_enterprises WHERE id = ?;", (address_id,))
        return cursor.fetchone()

def update(address_id, street=None, city=None, state=None, enterprise_id=None):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        fields, values = [], []

        if street:
            fields.append("street = ?")
            values.append(street)
        if city:
            fields.append("city = ?")
            values.append(city)
        if state:
            fields.append("state = ?")
            values.append(state)
        if enterprise_id:
            fields.append("enterprise_id = ?")
            values.append(enterprise_id)

        if not fields:
            return

        values.append(address_id)
        query = f"UPDATE addresses_enterprises SET {', '.join(fields)} WHERE id = ?;"
        cursor.execute(query, values)
        conn.commit()

def delete(address_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM addresses_enterprises WHERE id = ?;", (address_id,))
        conn.commit()
