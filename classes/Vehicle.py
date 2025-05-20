import os
from enum import Enum
from typing import Optional, Dict, Any

import sqlite3
from dotenv import load_dotenv
from openrouteservice import Client

from db.database import get_connection


class MaxDistance(Enum):
    ...
class VehicleType(Enum):
    """Enumeração para os tipos de veículos."""
    MOTO = "moto"
    CARRO = "carro"
    CAMINHAO = "caminhao"


class Vehicle:
    """
    Classe que representa um veículo.

    Atributos:
        model (str): Modelo do veículo.
        mark (str): Marca do veículo.
        plate (str): Placa do veículo (7 caracteres).
        type_vehicle (VehicleType): Tipo do veículo.
        maximum_distance (int): Distância máxima suportada.
    """

    def __init__(self, model: str, mark: str, plate: str, type_vehicle: VehicleType, maximum_distance: int = 0):
        self._model = model
        self._mark = mark
        self.plate = plate  # setter com validação
        self._maximum_distance = maximum_distance
        self.type_vehicle = type_vehicle  # setter com validação
        self._can_add_load = True

    @property
    def model(self) -> str:
        return self._model

    @model.setter
    def model(self, value: str) -> None:
        self._model = value

    @property
    def mark(self) -> str:
        return self._mark

    @mark.setter
    def mark(self, value: str) -> None:
        self._mark = value

    @property
    def plate(self) -> str:
        return self._plate

    @plate.setter
    def plate(self, value: str) -> None:
        if not isinstance(value, str) or len(value) != 7:
            raise ValueError("Placa deve ter exatamente 7 caracteres.")
        self._plate = value

    @property
    def maximum_distance(self) -> int:
        return self._maximum_distance

    @maximum_distance.setter
    def maximum_distance(self, value: int) -> None:
        self._maximum_distance = value

    @property
    def type_vehicle(self) -> VehicleType:
        return self._type_vehicle

    @type_vehicle.setter
    def type_vehicle(self, value: VehicleType) -> None:
        if not isinstance(value, VehicleType):
            raise ValueError("Tipo de veículo inválido.")
        self._type_vehicle = value


    #Criar lógica para verficar a distância por tipo de veículo
    def calculate_distance(self, origin: str, destination: str) -> Optional[Dict[str, str]]:
        """
        Calcula a distância e duração estimada entre dois endereços utilizando a API OpenRouteService.
        """
        load_dotenv(dotenv_path='.env')
        api_key = os.getenv("API_KEY")

        if not api_key:
            print("[Erro] Chave de API não encontrada no .env")
            return None

        client = Client(key=api_key)

        profile = "driving-car"
        if self.type_vehicle == VehicleType.CAMINHAO:
            profile = "driving-hgv"

        def geocode(address: str):
            try:
                result = client.pelias_search(text=address)
                coords = result['features'][0]['geometry']['coordinates']
                return tuple(coords)
            except (IndexError, KeyError):
                raise ValueError(f"Endereço inválido ou não encontrado: {address}")

        try:
            coords_origin = geocode(origin)
            coords_dest = geocode(destination)

            rota = client.directions(
                coordinates=[coords_origin, coords_dest],
                profile=profile,
                format='json'
            )

            distancia_km = rota['routes'][0]['summary']['distance'] / 1000
            duracao_horas = rota['routes'][0]['summary']['duration'] / 3600

            return {
                "distancia_km": f"{distancia_km:.2f}",
                "duracao_horas": f"{duracao_horas:.1f}"
            }

        except Exception as e:
            print(f"[Erro ao calcular rota] {e}")
            return None

    def get_max_capacity(self) -> int:
        """
        Retorna a capacidade máxima de carga com base no tipo do veículo.
        """
        if self.type_vehicle == VehicleType.MOTO:
            return 100
        elif self.type_vehicle == VehicleType.CARRO:
            return 200
        elif self.type_vehicle == VehicleType.CAMINHAO:
            return 1000
        return 0
    def insert(self, delivery_person_id: int) -> None:
        """
        Insere o veículo no banco de dados com o delivery_person_id.

        Args:
            delivery_person_id (int): ID do entregador associado ao veículo.
        """
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO vehicle (model, mark, plate, type_vehicle, maximum_distance, delivery_person_id)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (self.model, self.mark, self.plate, self.type_vehicle.value, self.maximum_distance, delivery_person_id))
            conn.commit()


    @staticmethod
    def get_all() -> list:
        """Retorna todos os veículos cadastrados."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicle;")
            return cursor.fetchall()

    @staticmethod
    def get_by_id(vehicle_id: int) -> Optional[tuple]:
        """Retorna um veículo pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vehicle WHERE id = ?;", (vehicle_id,))
            return cursor.fetchone()

    @staticmethod
    def update(vehicle_id: int, model= None, mark= None, plate= None,
               type_vehicle = None, maximum_distance = None, delivery_person_id = None) -> None:
        """
        Atualiza os dados de um veículo com base nos parâmetros fornecidos.
        """
        with get_connection() as conn:
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
                values.append(type_vehicle.value)
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
    def delete(vehicle_id: int) -> None:
        """Remove um veículo do banco de dados."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vehicle WHERE id = ?;", (vehicle_id,))
            conn.commit()

    def to_dict(self) -> Dict[str, Any]:
        """Retorna um dicionário com os atributos do veículo."""
        return {
            "model": self.model,
            "mark": self.mark,
            "plate": self.plate,
            "maximum_distance": self.maximum_distance,
            "type_vehicle": self.type_vehicle.value
        }

    def __str__(self) -> str:
        return f"{self.type_vehicle.value} vrum vrum: {self.model} {self.mark} {self.plate} {self.maximum_distance} km"
