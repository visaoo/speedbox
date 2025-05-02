
class Address:
    def __init__(self, rua, numero, bairro, cidade, estado):
        self._rua = rua
        self._numero = numero
        self._bairro = bairro
        self._cidade = cidade
        self._estado = estado

    @property
    def rua(self):
        return self._rua

    @rua.setter
    def rua(self, value):
        self._rua = value

    @property
    def numero(self):
        return self._numero

    @numero.setter
    def numero(self, value):
        self._numero = value

    @property
    def bairro(self):
        return self._bairro

    @bairro.setter
    def bairro(self, value):
        self._bairro = value

    @property
    def cidade(self):
        return self._cidade

    @cidade.setter
    def cidade(self, value):
        self._cidade = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    def __str__(self):
        return f'{self.rua}, {self.numero}, {self.bairro}, {self.cidade}, {self.estado}'


# origem = Address('Rua Folha Dourada', '6', 'Jardim Miragaia', 'São Paulo', 'SP')
# destino = Address('Rua Olivio Segatto', '1017', 'Centro', 'Tupi Paulista', 'SP')


# print(origem, destino)

# ford = Vehicle('model', 'mark', 'str', Vehicle_type.CARRO)


# print(ford.calculate_distance(origem, destino))
