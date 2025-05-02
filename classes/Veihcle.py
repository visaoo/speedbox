import os
from enum import Enum

from dotenv import load_dotenv
from openrouteservice import Client


class Vehicle_type(Enum):
    CARRO = "carro"
    MOTO = "moto"
    VAN = "van"
    CAMINHAO = "caminhao"


class Vehicle:
    def __init__(self, model: str, mark: str, plate: str, type: Vehicle_type):  # trocar str pra peso do item qnd tiver
        self._model = model
        self._mark = mark
        self._plate = plate
        self._maximum_load = []
        self._type_vehicle = type

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @property
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        self._mark = value

    @property
    def plate(self):
        return self._plate

    @plate.setter
    def plate(self, value):
        self._plate = value

    @property
    def maximum_load(self):
        return self._maximum_load

    @maximum_load.setter
    def maximum_load(self, value):
        self._maximum_load = value

    @property
    def type_vehicle(self):
        return self._type_vehicle

    @type_vehicle.setter
    def type_vehicle(self, value):
        self._type_vehicle = value

    def calculate_distance(self, origin, destination):
        load_dotenv(dotenv_path='.env')

        try:
            api_key = os.getenv("API_KEY")
            if not api_key:
                raise EnvironmentError('Chave de API não encontrada')
            client = Client(key=api_key)
        except EnvironmentError as e:
            print(f'[Erro]{e}')
            return

        profile = 'driving-car'
        if self.type_vehicle == Vehicle_type.CAMINHAO:
            profile = 'driving-hgv'

        # Geocodificação do endereço
        def geocodificate(endereco):
            try:
                resultado = client.pelias_search(text=endereco)
                coords = resultado['features'][0]['geometry']['coordinates']
                return tuple(coords)  # (lon, lat)
            except (IndexError, KeyError):
                raise ValueError(f"Endereço inválido ou não encontrado: {endereco}")
        try:
            _origin = geocodificate(origin)
            _destination = geocodificate(destination)
            rota = client.directions(
                coordinates=[_origin, _destination],
                profile=profile,
                format='json'
            )

            distance = rota['routes'][0]['summary']['distance'] / 1000  # km
            duration = rota['routes'][0]['summary']['duration'] / 3600  # minutos

            return {"distancia_km": f'{distance:.2f}', "duracao_horas": f'{duration:.1f}'}
        except Exception as e:
            print(f'[Erro ao calcular rota] {e}')
            return


# carro = Vehicle('palio', 'a', Vehicle_type.CARRO)


# # # Exemplo
# #         origem = geocodificar("Avenida Sapopemba, 1000, São Paulo, SP")
# #         destino = geocodificar("Praça da Sé, 111,São Paulo, SP")
# carro.calculate_distance('Av. Sapopemba, 1000, São Paulo, SP', 'Rua Olivio Segatto, 1017, Tupi Paulista, SP')
