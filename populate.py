import sqlite3 as sql
import random
from faker import Faker

fake = Faker("pt_BR")

def insert_data_faker(max_rows=100):
    with sql.connect("database.db") as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()

        client_ids = []
        product_ids = []
        order_ids = []
        address_ids = []

        # Inserindo dados na tabela `clients`
        for _ in range(max_rows):
            cursor.execute(
                """
                INSERT INTO clients (name, cpf, birth_date, user_id)
                VALUES (?, ?, ?, ?)
                """,
                (
                    fake.name(),
                    fake.cpf(),
                    fake.date_of_birth(minimum_age=18).strftime("%Y-%m-%d"),
                    fake.random_int(min=1, max=99999),
                ),
            )
            client_ids.append(cursor.lastrowid)

        # Inserindo dados na tabela `users`
        for _ in range(max_rows):
            cursor.execute(
                """
                INSERT INTO users (email, username, password, is_admin)
                VALUES (?, ?, ?, ?)
                """,
                (
                    fake.email(),
                    fake.user_name(),
                    fake.password(),
                    fake.random_int(min=0, max=1),
                ),
            )

        # Inserindo dados na tabela `products`
        for _ in range(max_rows):
            cursor.execute(
                """
                INSERT INTO products (name, price)
                VALUES (?, ?)
                """,
                (fake.word(), fake.random_number(digits=2)),
            )
            product_ids.append(cursor.lastrowid)

        # Inserindo dados na tabela `orders`
        for _ in range(max_rows):
            client_id = random.choice(client_ids)
            total = fake.random_number(digits=3)
            date = fake.date()

            cursor.execute(
                """
                INSERT INTO orders (client_id, total, date)
                VALUES (?, ?, ?)
                """,
                (client_id, total, date),
            )
            order_ids.append(cursor.lastrowid)

        # Inserindo dados na tabela `order_items`
        for _ in range(max_rows):
            order_id = random.choice(order_ids)
            product_id = random.choice(product_ids)
            quantity = fake.random_int(min=1, max=5)

            cursor.execute(
                """
                INSERT INTO order_items (order_id, product_id, quantity)
                VALUES (?, ?, ?)
                """,
                (order_id, product_id, quantity),
            )

        # Inserindo dados na tabela `addresses`
        for _ in range(max_rows):
            client_id = random.choice(client_ids)
            print(f"client_id: {client_id}")
            cursor.execute(
                """
                INSERT INTO addresses (street, city, state, zip_code, client_id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    fake.street_address(),
                    fake.city(),
                    fake.state_abbr(),
                    fake.postcode(),
                    client_id,
                ),
            )
            address_ids.append(cursor.lastrowid)

        # Inserindo dados na tabela `enterprises`
        for _ in range(max_rows):
            address_id = random.choice(address_ids)
            cursor.execute(
                """
                INSERT INTO enterprises (name, cnpj, address)
                VALUES (?, ?, ?)
                """,
                (fake.company(), fake.cnpj(), address_id),
            )

        conn.commit()

if __name__ == "__main__":
    qtd = int(input("Quantas linhas deseja inserir no banco? "))
    if qtd <= 0:
        print("Número inválido. Insira um número maior que zero.")
    else:
        insert_data_faker(qtd)
        print("Dados inseridos com sucesso!")