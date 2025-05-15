from transaction import Transaction

class Boleto(Transaction):
    def __init__(self, typeable_line):
        
        self._typeable_line = typeable_line

    @property
    def typeable_line(self):
        return self._typeable_line

    @typeable_line.setter
    def typeable_line(self, value):
        self._typeable_line = value
