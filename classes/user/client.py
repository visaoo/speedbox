from typing import List

from item import Item
from order import Order
from person import Person
from user import User


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

    def finalize_order(self, item: Item):
        if not self._cart:
            print("Carrinho vazio! Não é possível finalizar o pedido.")
            # remove print
            return

            # verificar a lógica com o pessoal pois vai precisar do resto do sistema antes de continuar os métodos

    def add_item(self, item: Item):
        self._cart.append(item)

def remove_item_by_id(self, item_id: str):
    """Recebe o id do item e o remove do sistema"""
    for item in self._cart:
        if item.id == item_id:
            self._cart.remove(item)
            return
    print("Item não encontrado no carrinho!")

    def cancel_order(self):
        self._cart.clear()


class ManageCustomer:
    pass  # crud
