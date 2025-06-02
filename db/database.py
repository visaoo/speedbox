import sqlite3

DB_PATH = "speedbox.db"


def get_connection():
    """Retorna uma conexão com o banco de dados para uso com with"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
