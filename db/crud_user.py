import sqlite3

def get_all():
    """
    Retorna todos os usuários cadastrados.
    """
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
        return cursor.fetchall()

def get_by_id(user_id):
    """
    Retorna um usuário pelo ID.
    """
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        return cursor.fetchone()

def update(user_id, email=None, username=None, password=None):
    """
    Atualiza dados de um usuário.
    """
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        fields = []
        values = []

        if email:
            fields.append("email = ?")
            values.append(email)
        if username:
            fields.append("username = ?")
            values.append(username)
        if password:
            fields.append("password = ?")
            values.append(password)
        if not fields:
            return  # Nada para atualizar

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?;"
        cursor.execute(query, values)
        conn.commit()

def delete(user_id):
    """
    Deleta um usuário do banco de dados.
    """
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?;", (user_id,))
        conn.commit()
