import sqlite3

def insert_user(email, username, password, is_admin=False):
    """
    Insere um novo usuário no banco de dados.
    """
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (email, username, password, is_admin)
            VALUES (?, ?, ?, ?);
            """,
            (email, username, password, is_admin)
        )
        conn.commit()

def get_all_users():
    """
    Retorna todos os usuários cadastrados.
    """
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
        return cursor.fetchall()

def get_user_by_id(user_id):
    """
    Retorna um usuário pelo ID.
    """
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?;", (user_id,))
        return cursor.fetchone()

def update_user(user_id, email=None, username=None, password=None, is_admin=None):
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
        if is_admin is not None:
            fields.append("is_admin = ?")
            values.append(is_admin)

        if not fields:
            return  # Nada para atualizar

        values.append(user_id)
        query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?;"
        cursor.execute(query, values)
        conn.commit()

def delete_user(user_id):
    """
    Deleta um usuário do banco de dados.
    """
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?;", (user_id,))
        conn.commit()
