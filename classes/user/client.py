from classes.item import Item
from classes.order import Order
from classes.user.person import Person
from classes.user.user import User
from classes.address.address import Address
from typing import List
# from db import database


########### tests
import sqlite3
database = sqlite3.connect(':memory:') 

cursor = database.cursor()
database.commit()

# Criando a tabela `cart_items`
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_cpf TEXT,
        item_id TEXT,
        name TEXT,
        price REAL
    )
''')

class Client(Person):
    def __init__(self, name, cpf, address, birth_date, order_history: List[Order], cart: List[Item], user: User):
        super().__init__(name, cpf, address, birth_date)

        self._order_history = order_history
        self._cart = cart
        self._user = user

    @property
    def order_history(self):
        return self._order_history

    @property
    def cart(self):
        return self._cart

    @property
    def user(self):
        return self._user

    def save_to_db(self):
        database.execute('''
            INSERT OR REPLACE INTO clients (name, cpf, address, birth_date, user_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.name, self.cpf, self.address, self.birth_date, self._user.id))
        database.commit()

    def add_item(self, item: Item):
        self._cart.append(item)
        print(f"Item {item.id} adicionado ao carrinho.")
        database.execute('''
            INSERT INTO cart_items (client_cpf, item_id, name, price)
            VALUES (?, ?, ?, ?)
        ''', (self.cpf, item.id, item.name, item.price))
        database.commit()

    def remove_item_by_id(self, item_id: str):
        for item in self._cart:
            if item.id == item_id:
                self._cart.remove(item)
                database.execute('DELETE FROM cart_items WHERE client_cpf = ? AND item_id = ?', (self.cpf, item_id))
                database.commit()
                return
        print("Item não encontrado no carrinho!")

    def cancel_order(self):
        self._cart.clear()
        database.execute('DELETE FROM cart_items WHERE client_cpf = ?', (self.cpf,))
        database.commit()

    def finalize_order(self):
        if not self._cart:
            return { "error": "Carrinho vazio!" }

        total = sum(item.price for item in self._cart)

        # Salva o pedido
        database.execute('''
            INSERT INTO orders (client_cpf, total, date)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (self.cpf, total))
        database.commit()

        # Limpa o carrinho
        self.cancel_order()


cliente1 = Client("João", "12345678901", Address('Rua A', '1234', '1', 'skylake', 'massacheetos'), "1990-01-01", [], [], User("joao", "joao123@gmail.com", "senha123"))

cliente1.add_item(Item("Produto 1", 20, 10.0, "1", "Produto 1", "Descrição do Produto 1"))
cliente1.add_item(Item("Produto 2", 21, 20.0, "1", "Produto 2", "Descrição do Produto 2"))

print(cliente1.cart)  
