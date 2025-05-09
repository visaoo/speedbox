import sqlite3 as sq

__conn = sq.connect('speedbox.db')
__cursor = sq.Cursor()


def create_table_enterprise():
    __cursor.execute('''
                     CREATE TABLE IF NOT EXISTS empresas(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cnpj TEXT NOT NULL,
                        pix TEXT NOT NULL, 
                     )
                     ''')