import sqlite3 as sq

def create_address_table():
    with sq.connect("speedbox.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS address (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                street TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                zip_code TEXT NOT NULL
            )
        ''')
        conn.commit()

def create_address(street, city, state, zip_code):
    with sq.connect("speedbox.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO address (street, city, state, zip_code) 
            VALUES (?, ?, ?, ?)
        ''', (street, city, state, zip_code))
        conn.commit()
        return cursor.lastrowid
    
def update_address(address_id, street, city, state, zip_code):
    with sq.connect("speedbox.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE address SET street = ?, city = ?, state = ?, zip_code = ? WHERE id = ?
        ''', (street, city, state, zip_code, address_id))
        conn.commit()
        return cursor.rowcount > 0
    
def delete_address(address_id):
    with sq.connect("speedbox.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM address WHERE id = ?
        ''', (address_id,))
        conn.commit()
        return cursor.rowcount > 0


# testes banco de dados

if __name__ == "__main__":
    create_address_table()
    
    address_id = create_address("234 Main St", "Springfield", "IL", "62471")
    print(f"Created address with ID: {address_id}")
    updated = update_address(address_id, "992 Elm St", "Springfield", "IL", "62003")
    print(f"Updated address: {updated}")
    deleted = delete_address(address_id)
    print(f"Deleted address: {deleted}")