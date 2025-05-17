import sqlite3

def insert_address_client(street, city, state, client_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO addresses_clients (street, city, state, client_id)
            VALUES (?, ?, ?, ?);
        """, (street, city, state, client_id))
        conn.commit()

def get_all_addresses_clients():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM addresses_clients;")
        return cursor.fetchall()

def get_address_client_by_id(address_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM addresses_clients WHERE id = ?;", (address_id,))
        return cursor.fetchone()

def update_address_client(address_id, street=None, city=None, state=None, client_id=None):
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
        if client_id:
            fields.append("client_id = ?")
            values.append(client_id)

        if not fields:
            return

        values.append(address_id)
        query = f"UPDATE addresses_clients SET {', '.join(fields)} WHERE id = ?;"
        cursor.execute(query, values)
        conn.commit()

def delete_address_client(address_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM addresses_clients WHERE id = ?;", (address_id,))
        conn.commit()
