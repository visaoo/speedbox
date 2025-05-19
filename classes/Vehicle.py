import os
from enum import Enum
import sqlite3

from dotenv import load_dotenv
from openrouteservice import Client

import sqlite3


class VehicleType(Enum):
    MOTO = "moto"
    CARRO = "carro"
    CAMINHAO = "caminhao"


class Vehicle:

    def __init__(self, model: str, mark: str, plate: str, type_vehicle: VehicleType, maximum_distance: int = 0):
        self._model = model
        self._mark = mark
        self._plate = plate
        self._maximum_distance = maximum_distance
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
    def maximum_distance(self):
        return self._maximum_distance

    @maximum_distance.setter
    def maximum_distance(self, value):
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
        
    def get_max_capacity(self, aaaaa) -> int:
        tipo = self.type_vehicle
        if tipo == VehicleType.MOTO:
            return 100
        elif tipo == VehicleType.CARRO:
            return 200
        elif tipo == VehicleType.CAMINHAO:
            return 1000
        return 0

    
    
    def insert(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vehicle (model, mark, plate, type_vehicle, maximum_distance)
                VALUES (?, ?, ?, ?, ?);
            """, (self.model, self.mark, self.plate, self.type_vehicle, self.maximum_distance))
            conn.commit()

    @staticmethod
    def get_all():
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicle;")
            return cursor.fetchall()

    @staticmethod
    def get_by_id(vehicle_id):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicle WHERE id = ?;", (vehicle_id,))
            return cursor.fetchone()

    @staticmethod
    def update(vehicle_id, model=None, mark=None, plate=None, type_vehicle=None, maximum_distance=None, delivery_person_id=None):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            fields, values = [], []

            if model:
                fields.append("model = ?")
                values.append(model)
            if mark:
                fields.append("mark = ?")
                values.append(mark)
            if plate:
                fields.append("plate = ?")
                values.append(plate)
            if type_vehicle:
                fields.append("type_vehicle = ?")
                values.append(type_vehicle)
            if maximum_distance:
                fields.append("maximum_distance = ?")
                values.append(maximum_distance)
            if delivery_person_id:
                fields.append("delivery_person_id = ?")
                values.append(delivery_person_id)

            if not fields:
                return

            values.append(vehicle_id)
            query = f"UPDATE vehicle SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, values)
            conn.commit()
            
    @staticmethod
    def delete(vehicle_id):
            with sqlite3.connect("database.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM vehicle WHERE id = ?;", (vehicle_id,))
                conn.commit()

        
        
    def to_dict(self):
        return {
            "model": self._model,
            "mark": self._mark,
            "plate": self._plate,
            "maximum_load": self._maximum_load,
            "type_vehicle": self._type_vehicle.value
        }
        
    def __str__(self):
        return f'{self._type_vehicle.value} vrum vrum: {self._model} {self._mark} {self._plate} {self._maximum_load}'
