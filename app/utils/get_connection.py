import sqlite3


# Função auxiliar para conexão com o banco
def get_connection():
    conn = sqlite3.connect("database.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
