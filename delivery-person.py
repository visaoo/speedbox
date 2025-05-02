from typing import List
from person import Person
from order import Order
from vehicle import Vehicle

class DeliveryPerson(Person):
    def __init__(self, name, cpf, address, birth_date, cnh: None, available: bool, vehicle: List[Vehicle], accepted_orders: List[Order]):
        super().__init__(name, cpf, address, birth_date)
        self._cnh = cnh
        self._available = available
        self._vehicle = vehicle
        self._accepted_orders = accepted_orders

        @property
        def cnh(self):
            return self._cnh

        @property
        def available(self):
            return self._available

        @available.setter
        def available(self, value):
            self._available = value

        @property
        def vehicle(self):
            return self._vehicle

        @vehicle.setter
        def vehicle(self, value):
            self._vehicle = value

        @property
        def accepted_orders(self):
            return self._accepted_orders

        @accepted_orders.setter
        def accepted_orders(self, value):
            self._accepted_orders = value

        def accept_order(self, order: Order):
            if self.available:
                self._accepted_orders.append(order)
                self.available = False
                return f"Pedido {order} aceito."
            else:
                return f"{self.name} precisa entregar o pedido aceito."

class DeliveryCustomer:
    pass # crud