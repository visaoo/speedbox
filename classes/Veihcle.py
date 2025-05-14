import os
from enum import Enum

from dotenv import load_dotenv
from openrouteservice import Client

from sqlalchemy import (Column, Integer, ForeignKey, String, Boolean)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
Base = declarative_base()

class VehicleType(Enum):
    MOTO = "moto"
    CARRO = "carro"
    CAMINHAO = "caminhao"

class Vehicle(Base):
    __tablename__ = 'veiculos'

    id_vehicle = Column(Integer, primary_key=True, autoincrement=True)
    _model = Column("model", String(15))
    _mark = Column("mark", String(15))
    _plate = Column("plate", String(7))
    _maximum_load = Column("maximum_load", Integer, default=0)
    is_max = Column(Boolean, default=True)
    _type_vehicle = Column("type_vehicle", Enum(VehicleType))

    delivery_person_id = Column(Integer, ForeignKey('delivery_person.id'))
    delivery_person = relationship('Delivery_person', back_populates='veiculos')



    def __init__(self, model: str, mark: str, plate: str, type_vehicle: VehicleType, maximum_load: int = 0):
        self.model = model
        self.mark = mark
        self.plate = plate
        self.maximum_load = maximum_load
        self.type_vehicle = type_vehicle
        self._can_add_load = True  # usado internamente

    @hybrid_property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    @hybrid_property
    def mark(self):
        return self._mark

    @mark.setter
    def mark(self, value):
        self._mark = value

    @hybrid_property
    def plate(self):
        return self._plate

    @plate.setter
    def plate(self, value):
        if not isinstance(value, str) or len(value) != 7:
            raise ValueError("Placa deve ter exatamente 7 caracteres.")
        self._plate = value

    @hybrid_property
    def maximum_load(self):
        return self._maximum_load

    @maximum_load.setter
    def maximum_load(self, value):
        if value < 0:
            raise ValueError("Carga máxima não pode ser negativa.")
        self._maximum_load = value

    @hybrid_property
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