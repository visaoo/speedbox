import sqlite3

DB_PATH = "speedbox.db"


def get_connection():
    """Retorna uma conexão com o banco de dados para uso com with"""
    return sqlite3.connect(DB_PATH)
