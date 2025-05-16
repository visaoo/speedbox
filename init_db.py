import sqlite3 as sql
import populate

sql.connect("database.db")


# Criando nossas tabelitas
def create_tables():
    with sql.connect("database.db") as conn:
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = ON")

        # Criando a tabela `clients`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            birth_date TEXT,
            user_id INTEGER
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
        )

        # Criando a tabela `products`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            enterprise_id INTEGER NOT NULL,
            FOREIGN KEY (enterprise_id) REFERENCES enterprises(id) ON DELETE CASCADE
        );
        """
        )

        # Criando a tabela `orders`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL,
            date TEXT,
            client_id INTEGER NOT NULL,
            status ENUM('payment_pending', 'pending', 'completed', 'canceled') DEFAULT 'pending',
            FOREIGN KEY (client_id) REFERENCES clients(id)
        );
        """
        )

        # Criando a tabela `order_items`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
        """
        )
        # Criando a tabela `users`
        cursor.execute(  # coloquei is_admin para test, se sobrar tempo implementar
            """
            CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
        );
        """
        )
        # Criando a tabela `addresses_clients`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS addresses_clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            street TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            postcode TEXT NOT NULL,
            client_id INTEGER NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
        );
        """
        )
        # Criando a tabela `Addresses_enterprises`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS addresses_enterprises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            street TEXT NOT NULL,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            postcode TEXT NOT NULL,
            enterprise_id INTEGER NOT NULL,
            FOREIGN KEY (enterprise_id) REFERENCES enterprises(id) ON DELETE CASCADE
        );
        """
        )
        # Criando a tabela `enterprises`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS enterprises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cnpj TEXT UNIQUE NOT NULL
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        """
        )

        # Criando a tabela `delivery_person`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS delivery_person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
    """
        )


if __name__ == "__main__":
    create_tables()
    print("Tabelas criadas com sucesso!")

    r_user = input("Deseja popular as tabelas com dados de teste? (s/n): ")
    r_qtd = input("Quantas linhas deseja inserir? (padrão 10): ")
    r_qtd = int(r_qtd) if r_qtd.isdigit() else 10
    if r_user.lower() == "s":
        populate.insert_data_faker(r_qtd)
        print("Dados de teste inseridos com sucesso!")
