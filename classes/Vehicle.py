import os
from enum import Enum

from dotenv import load_dotenv
from openrouteservice import Client


class VehicleType(Enum):
    MOTO = "moto"
    CARRO = "carro"
    CAMINHAO = "caminhao"


class Vehicle:

    def __init__(self, model: str, mark: str, plate: str, type_vehicle: VehicleType, maximum_load: int = 0):
        self._model = model
        self._mark = mark
        self._plate = plate
        self._maximum_load = maximum_load
        self._type_vehicle = type_vehicle
        self._can_add_load = True  # usado internamente

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
        if not isinstance(value, str) or len(value) != 7:
            raise ValueError("Placa deve ter exatamente 7 caracteres.")
        self._plate = value

    @property
    def maximum_load(self):
        return self._maximum_load

    @maximum_load.setter
    def maximum_load(self, value):
        if value < 0:
            raise ValueError("Carga máxima não pode ser negativa.")
        self._maximum_load = value

    @property
    def type_vehicle(self):
        return self._type_vehicle

    @type_vehicle.setter
    def type_vehicle(self, value):
        if not isinstance(value, VehicleType):
            raise ValueError("Tipo de veículo inválido.")
        self._type_vehicle = value

    def calculate_distance(self, origin: str, destination: str):
        load_dotenv(dotenv_path='.env')

        try:
            api_key = os.getenv("API_KEY")
            if not api_key:
                raise EnvironmentError('Chave de API não encontrada')
            client = Client(key=api_key)
        except EnvironmentError as e:
            print(f'[Erro] {e}')
            return

        profile = 'driving-car'
        if self.type_vehicle == VehicleType.CAMINHAO:
            profile = 'driving-hgv'

        def geocodificate(endereco):
            try:
                resultado = client.pelias_search(text=endereco)
                coords = resultado['features'][0]['geometry']['coordinates']
                return tuple(coords)
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
            duration = rota['routes'][0]['summary']['duration'] / 3600  # horas

            return {"distancia_km": f'{distance:.2f}', "duracao_horas": f'{duration:.1f}'}
        except Exception as e:
            print(f'[Erro ao calcular rota] {e}')
            return

    def can_add_load(self, peso: int) -> bool:
        return self.maximum_load + peso <= self.get_max_capacity()

    def get_max_capacity(self) -> int:
        tipo = self.type_vehicle
        if tipo == VehicleType.MOTO:
            return 50
        elif tipo == VehicleType.CARRO:
            return 200
        elif tipo == VehicleType.CAMINHAO:
            return 1000
        return 0
