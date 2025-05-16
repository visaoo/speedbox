from transaction import Transaction

class Boleto:
    def __init__(self, amount: float, due_date: str, payer_name: str):
        self.due_date = due_date
        self.payer_name = payer_name

    