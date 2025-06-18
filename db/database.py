from sqlite3 import connect, Connection, Error

DB_PATH = "speedbox.db"


def get_connection() -> Connection:
    """
    Estabelece uma conexão com o banco de dados SQLite.
    Retorna uma conexão, levanta uma exceção em caso de erro.
    """
    try:
        conn = connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise e
