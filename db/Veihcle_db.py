import sqlite3 as sq

def create_table_vehicle():
    with sq.connect('speedbox.db') as conn:
        conn.execute("PRAGMA foreign_keys = ON")  # habilita suporte a FK
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS veiculos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                modelo TEXT NOT NULL,
                placa TEXT NOT NULL,
                marca TEXT NOT NULL,
                tipo TEXT NOT NULL,
                carregado INTEGER,
                id_entregador INTEGER,
                FOREIGN KEY (id_entregador) REFERENCES entregadores(id)
            )
        ''')
        conn.commit()


def add_vehicle(model, plate, mark, type_, load):
    with sq.connect('speedbox.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO veiculos (modelo, placa, marca, tipo, carregado) 
            VALUES (?, ?, ?, ?, ?)
        ''', (model, plate, mark, type_, load))
        conn.commit()


def update_load(status, vehicle_id):
    with sq.connect('speedbox.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE veiculos SET carregado = ? WHERE id = ?
        ''', (status, vehicle_id))
        conn.commit()


def delete_vehicle(vehicle_id):
    try:
        with sq.connect('speedbox.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM veiculos WHERE id = ?
            ''', (vehicle_id,))
            conn.commit()
    except Exception as e:
        print(f'ERRO: {e}')


def search_vehicles():
    with sq.connect('speedbox.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM veiculos')
        return cursor.fetchall()
