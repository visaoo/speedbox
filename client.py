from typing import List

from item import Item
from order import Order

from person import Person


class Client(Person):
    def __init__(self, name, cpf, address, birth_date, order_history: List[Order], cart: List[Item]):
        super().__init__(name, cpf, address, birth_date)

        self._order_history = order_history
        self._cart = cart

    @property
    def order_history(self):
        return self._order_history

    @property
    def cart(self):
        return self._cart

    @cart.setter
    def cart(self, value):
        self._cart = value

    def finalize_order(self, item: Item):
        if not self._cart:
            print("Carrinho vazio! Não é possível finalizar o pedido.")
            # remove print
            return

            # verificar a lógica com o pessoal pois vai precisar do resto do sistema antes de continuar os métodos

    def add_item(self, item: Item):
        self._cart.append(item)

    def remove_item(self, item: Item):
        if item in self._cart:
            self._cart.remove(item)
        else:
            print("Carrinho vazio! Não é possível remover o pedido.")

    def cancel_order(self):
        self._cart.clear()


class ManageCustomer:
    pass  # crud
