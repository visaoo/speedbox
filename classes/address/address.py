import sqlite3

from db.database import get_connection


class Address:
    def __init__(
        self,
        street: str,
        number: str,
        neighborhood: str,
        city: str,
        state: str,
        client_id=None,
        enterprise_id=None,
        delivery_person_id=None
    ) -> None:
        self._street = street
        self._number = number
        self._neighborhood = neighborhood
        self._city = city
        self._state = state
        self._client_id = client_id
        self._enterprise_id = enterprise_id
        self._delivery_person_id = delivery_person_id

    @property
    def street(self) -> str:
        return self._street

    @property
    def number(self) -> str:
        return self._number

    @property
    def neighborhood(self) -> str:
        return self._neighborhood

    @property
    def city(self) -> str:
        return self._city

    @property
    def state(self) -> str:
        return self._state

    @street.setter
    def street(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("Street must be a non-empty string")
        self._street = value

    @number.setter
    def number(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("Number must be a non-empty string")
        self._number = value

    @neighborhood.setter
    def neighborhood(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("Neighborhood must be a non-empty string")
        self._neighborhood = value

    @city.setter
    def city(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("City must be a non-empty string")
        self._city = value

    @state.setter
    def state(self, value: str) -> None:
        if not value or not isinstance(value, str):
            raise ValueError("State must be a non-empty string")
        self._state = value

    def insert_address(self, type_user, client_id=None):
        with sqlite3.connect("speedbox.db") as conn:
            cursor = conn.cursor()
            if type_user.lower() == 'enterprise':
                cursor.execute("""
                    INSERT INTO addresses_enterprises (street, number, neighborhood, city, state, ,enterprise_id)
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (self.street, self.city, self.state))
                conn.commit()
            elif type_user.lower() == 'client':
                cursor.execute("""
                    INSERT INTO addresses_clients (street, number, neighborhood, city, state, client_id)
                VALUES (?, ?, ?, ?, ?);
                """, (self.street, self.number, self.neighborhood, self.city, self.state, client_id))
                conn.commit()
            else:
                raise ValueError("Invalid type_user. Must be 'enterprise' or 'client'.")

    @staticmethod
    def get_all(type_user):
        with get_connection() as conn:
            cursor = conn.cursor()
            if type_user.lower() == 'enterprise':
                cursor.execute("SELECT * FROM addresses_enterprises;")
                return cursor.fetchall()
            elif type_user.lower() == 'client':
                cursor.execute("SELECT * FROM addresses_clients;")
                return cursor.fetchall()
            else:
                raise ValueError("Invalid type_user. Must be 'enterprise' or 'client'.")

    @staticmethod
    def get_address_by_id(id, type_user):
        with get_connection() as conn:
            cursor = conn.cursor()
            if type_user.lower() == 'enterprise':
                cursor.execute("SELECT * FROM addresses_enterprises WHERE id = ?;", (id,))
                return cursor.fetchone()
            elif type_user.lower() == 'client':
                cursor.execute("SELECT * FROM addresses_clients WHERE id = ?;", (id,))
                return cursor.fetchone()

    @staticmethod
    def update_enterprise(id, type_user, street=None, city=None, state=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            fields, values = [], []

            if street:
                fields.append("street = ?")
                values.append(street)
            if city:
                fields.append("city = ?")
                values.append(city)
            if state:
                fields.append("state = ?")
                values.append(state)
            if not fields:
                return

            values.append(id)
            if type_user.lower() == 'enterprise':
                query = f"UPDATE addresses_enterprises SET {', '.join(fields)} WHERE id = ?;"
            elif type_user.lower() == 'client':
                query = f"UPDATE addresses_clients SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, values)
            conn.commit()

    @staticmethod
    def delete_enterprise(id, type_user):
        with get_connection() as conn:
            cursor = conn.cursor()
            if type_user.lower() == 'enterprise':
                cursor.execute("DELETE FROM addresses_enterprises WHERE id = ?;", (id,))
                conn.commit()
            elif type_user.lower() == 'client':
                cursor.execute("DELETE FROM addresses_clients WHERE id = ?;", (id,))
                conn.commit()

    def to_dict(self) -> dict:
        return {
            "street": self._street,
            "number": self._number,
            "neighborhood": self._neighborhood,
            "city": self._city,
            "state": self._state
        }

    def __str__(self) -> str:
        return f"{self._street}, {self._number}, {self._neighborhood}, {self._city}, {self._state}"
