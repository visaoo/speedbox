class Address:
    def __init__(
        self,
        street: str,
        number: str,
        neighborhood: str,
        city: str,
        state: str
    ) -> None:
        self._street = street
        self._number = number
        self._neighborhood = neighborhood
        self._city = city
        self._state = state

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

    def __str__(self) -> str:
        return f"{self._street}, {self._number}, {self._neighborhood}, {self._city}, {self._state}"