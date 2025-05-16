from classes.item import Item
from classes.order import Order
from classes.user.person import Person
from classes.user.user import User
from classes.address.address import Address
from typing import List

from db import database

class Client(Person):
    def __init__(
        self,
        name,
        cpf,
        address,
        birth_date,
        order_history: List[Order],
        cart: List[Item],
        user: User,
    ):
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
        database.execute(
            """
            INSERT OR REPLACE INTO clients (name, cpf, birth_date, user_id)
            VALUES (?, ?, ?, ?)
        """,
            (self.name, self.cpf, self.address, self.birth_date, self._user.id),
        )
        database.commit()

    def add_item(self, item: Item):
        self._cart.append(item)
        print(f"Item {item.id} adicionado ao carrinho.")
        database.execute(
            """
            INSERT INTO cart_items (client_cpf, item_id, name, price)
            VALUES (?, ?, ?, ?)
        """,
            (self.cpf, item.id, item.name, item.price),
        )
        database.commit()

    def remove_item_by_id(self, item_id: str):
        for item in self._cart:
            if item.id == item_id:
                self._cart.remove(item)
                print(f"Item {item.id} removido do carrinho.")
                database.execute(
                    "DELETE FROM cart_items WHERE client_cpf = ? AND item_id = ?",
                    (self.cpf, item_id),
                )
                database.commit()
                return
        print("Item não encontrado no carrinho!")

    def cancel_order(self):
        self._cart.clear()
        database.execute("DELETE FROM cart_items WHERE client_cpf = ?", (self.cpf,))
        database.commit()

    def finalize_order(self):
        if not self._cart:
            return {"error": "Carrinho vazio!"}

        total = sum(item.price for item in self._cart)

        # Salva o pedido
        database.execute(
            """
            INSERT INTO orders (client_cpf, total, date)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """,
            (self._cpf, total),
        )
        database.commit()

        print(f"Pedido finalizado! Total: R${total:.2f}")

        # Limpa o carrinho
        self.cancel_order()