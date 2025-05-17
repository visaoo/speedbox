import sqlite3

def insert_client(name, cpf, birth_date, user_id):
    """
    Função para inserir um cliente no banco de dados.
    """
    with sqlite3.connect("../database.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO clients (name, cpf, birth_date, user_id)
            VALUES (?, ?, ?, ?);
            """,
            (name, cpf, birth_date, user_id),
        )
        conn.commit()

def get_all_clients():
    """
    Função para obter todos os clientes do banco de dados.
    """
    with sqlite3.connect("../database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients;")
        clients = cursor.fetchall()
    return clients

def get_client_by_id(client_id):
    """
    Função para obter um cliente pelo ID.
    """
    with sqlite3.connect("../database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clients WHERE id = ?;", (client_id,))
        client = cursor.fetchone()
    return client

def update_client(client_id, name=None, cpf=None, birth_date=None):
    """
    Função para atualizar um cliente no banco de dados.
    """
    with sqlite3.connect("../database.db") as conn:
        cursor = conn.cursor()

        fields = []
        values = []

        if name:
            fields.append("name = ?")
            values.append(name)
        if cpf:
            fields.append("cpf = ?")
            values.append(cpf)
        if birth_date:
            fields.append("birth_date = ?")
            values.append(birth_date)

        if not fields:
            return  # Nenhum campo para atualizar

        values.append(client_id)
        query = f"UPDATE clients SET {', '.join(fields)} WHERE id = ?;"
        cursor.execute(query, values)
        conn.commit()

def delete_client(client_id):
    """
    Função para deletar um cliente do banco de dados.
    """
    with sqlite3.connect("../database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM clients WHERE id = ?;", (client_id,))
        conn.commit()
