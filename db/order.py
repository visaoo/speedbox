import sqlite3 as sq


def create_table_order():
    with sq.connect('speedbox.db') as conn:
        conn.execute("PRAGMA foreign_keys = ON")  # habilita suporte a FK
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER,
                id_entregador INTEGER,
                status TEXT NOT NULL,
                FOREIGN KEY (id_cliente) REFERENCES clientes(id),
                FOREIGN KEY (id_entregador) REFERENCES entregadores(id)
            )
        ''')
        conn.commit()


def create_order(id_cliente, id_entregador, status):
    with sq.connect('speedbox.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO pedidos (id_cliente, id_entregador, status) 
            VALUES (?, ?, ?)
        ''', (id_cliente, id_entregador, status or 'Pendente'))
        conn.commit()
        return cursor.lastrowid


def update_order_status(order_id, status):
    with sq.connect('speedbox.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pedidos SET status = ? WHERE id = ?
        ''', (status, order_id))
        conn.commit()
        return cursor.rowcount > 0


def search_orders():
    with sq.connect('speedbox.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pedidos')
        return cursor.fetchall()
