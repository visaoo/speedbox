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

        # Criando a tabela `orders_clients`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL,
            date TEXT,
            client_id INTEGER NOT NULL,
            delivery_person_id INTEGER, NOT NULL,
            addrss_final TEXT NOT NULL,
            addrss_initial TEXT NOT NULL,
            status ENUM('payment_pending', 'pending', 'completed', 'canceled') DEFAULT 'pending',
            FOREIGN KEY (delivery_person_id) REFERENCES delivery_person(id),
            FOREIGN KEY (client_id) REFERENCES clients(id)
        );
        """
        )
        # Criando a tabela `orders_enterprises`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS orders_enterprises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total REAL,
            date TEXT,
            enterprise_id INTEGER NOT NULL,
            delivery_person_id INTEGER, NOT NULL,
            addrss_final TEXT NOT NULL,
            addrss_initial TEXT NOT NULL,
            status ENUM('payment_pending', 'pending', 'completed', 'canceled') DEFAULT 'pending',
            FOREIGN KEY (delivery_person_id) REFERENCES delivery_person(id),
            FOREIGN KEY (enterprise_id) REFERENCES enterprises(id)
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
    
        # criando a tabela `transactions`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_method ENUM('card', 'boleto', 'pix') NOT NULL,
            status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
            order_enterprise_id INTEGER,
            order_client_id INTEGER,
            FOREIGN KEY (order_client_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (order_enterprise_id) REFERENCES orders_enterprises(id) ON DELETE CASCADE
        );
        """
        )
        # Criando a tabela `card`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS card (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            number TEXT NOT NULL,
            validity TEXT NOT NULL,
            cvc TEXT NOT NULL,
            flag ENUM('visa', 'mastercard', 'elo', 'amex') NOT NULL,
            transaction_id INTEGER NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
        );
        """
        )
        # Criando a tabela `pix`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS pix (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT NOT NULL,
            transaction_id INTEGER NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
        );
        """
        )
    
        # Criando a tabela `boleto`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS boleto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            due_date TEXT NOT NULL,
            typeline TEXT NOT NULL,
            transaction_id INTEGER NOT NULL,
            FOREIGN KEY (transaction_id) REFERENCES transactions(id) ON DELETE CASCADE
        );
        """
        )
        
        # Criando a tabela `vehicle`
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vehicle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT NOT NULL,
            mark TEXT NOT NULL,
            plate TEXT UNIQUE,
            type_vehicle ENUM('bicicleta','moto', 'carro', 'caminhao') NOT NULL,
            maximum_distance ENUM('municipal', 'estadual', 'inter_estadual') NOT NULL,
            delivery_person_id INTEGER NOT NULL,
            FOREIGN KEY (delivery_person_id) REFERENCES delivery_person(id) ON DELETE CASCADE
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
