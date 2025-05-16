import sqlite3


import sqlite3

def insert_products(name, enterprise_id, description, price, stock):
    """
    Função para inserir produtos de teste no banco de dados.
    """
    with sqlite3.connect("../database.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO products (name, description, price, stock, enterprise_id)
            VALUES (?, ?, ?, ?, ?);
            """,
            (name, description, price, stock, enterprise_id),
        )
        conn.commit()

def get_all_products():
    """
    Função para obter todos os produtos do banco de dados.
    """
    with sqlite3.connect("../database.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products;")
        products = cursor.fetchall()

    return products

def get_product_by_id(product_id):
    """
    Função para obter um produto pelo ID.
    """
    with sqlite3.connect("../database.db") as conn: 
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products WHERE id = ?;", (product_id,))
        product = cursor.fetchone()

    return product

def update_product(product_id, name=None, description=None, price=None, stock=None):
    """
    Função para atualizar um produto no banco de dados.
    """
    with sqlite3.connect("../database.db") as conn:
        cursor = conn.cursor()

        # Cria uma lista com os campos a serem atualizados
        fields = []
        values = []

        if name:
            fields.append("name = ?")
            values.append(name)
        if description:
            fields.append("description = ?")
            values.append(description)
        if price:
            fields.append("price = ?")
            values.append(price)
        if stock:
            fields.append("stock = ?")
            values.append(stock)

        # Adiciona o ID do produto à lista de valores
        values.append(product_id)

        # Monta a query de atualização
        query = f"UPDATE products SET {', '.join(fields)} WHERE id = ?;"

        cursor.execute(query, values)
        conn.commit()
        
def delete_product(product_id):
    """
    Função para deletar um produto do banco de dados.
    """
    with sqlite3.connect("../database.db") as conn:
        cursor = conn.cursor()

        cursor.execute("DELETE FROM products WHERE id = ?;", (product_id,))
        conn.commit()