from typing import List, Optional

from order import Order
from person import Person
from user import User
from Vehicle import Vehicle
from db.database import get_connection
from address.address import Address


class DeliveryPerson(Person):
    def __init__(
        self,
        name: str,
        cpf: str,
        address: Address,
        birth_date: str,
        cnh: str,
        available: bool,
        vehicle: Vehicle,
        user: User,
        phone: str
    ) -> None:
        """
        Inicializa um entregador com informações pessoais, CNH, veículo, usuário e disponibilidade.

        Args:
            name (str): Nome completo.
            cpf (str): CPF.
            address (Address): Endereço.
            birth_date (str): Data de nascimento.
            cnh (str): Número da CNH.
            available (bool): Disponibilidade.
            vehicle (Vehicle): Veículo utilizado.
            user (User): Objeto do usuário vinculado.
            phone (str): Número de telefone.
        """
        super().__init__(name, cpf, address, birth_date)
        self._cnh: str = cnh
        self._available: bool = available
        self._vehicle: Vehicle = vehicle
        self._accepted_orders: List[Order] = []
        self._user: User = user
        self.phone: str = phone

    @property
    def cnh(self) -> str:
        """Retorna o número da CNH do entregador."""
        return self._cnh

    @property
    def available(self) -> bool:
        """Retorna se o entregador está disponível."""
        return self._available

    @available.setter
    def available(self, value: bool) -> None:
        """Define a disponibilidade do entregador."""
        if not isinstance(value, bool):
            raise ValueError("O valor de 'available' deve ser um booleano.")
        self._available = value

    @property
    def vehicle(self) -> Vehicle:
        """Retorna o veículo do entregador."""
        return self._vehicle

    @vehicle.setter
    def vehicle(self, value: Vehicle) -> None:
        """Atualiza o veículo do entregador."""
        self._vehicle = value

    @property
    def accepted_orders(self) -> List[Order]:
        """Retorna a lista de pedidos aceitos pelo entregador."""
        return self._accepted_orders

    @accepted_orders.setter
    def accepted_orders(self, value: List[Order]) -> None:
        """Define a lista de pedidos aceitos."""
        self._accepted_orders = value

    @property
    def user(self) -> User:
        """Retorna o usuário associado ao entregador."""
        return self._user

    @user.setter
    def user(self, value: User) -> None:
        """Atualiza o usuário associado."""
        if not isinstance(value, User):
            raise ValueError("O valor deve ser uma instância de User.")
        self._user = value

    def insert(self) -> None:
        """
        Insere o entregador no banco de dados.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO delivery_person (name, cpf, cnh, birth_date, celphone)
                VALUES (?, ?, ?, ?, ?);
                """,
                (self.name, self.cpf, self.cnh, self.birth_date, self.phone)
            )
            conn.commit()

    @staticmethod
    def get_all() -> List[tuple]:
        """
        Retorna todos os entregadores cadastrados.

        Returns:
            List[tuple]: Lista de tuplas com os dados dos entregadores.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM delivery_person;")
            return cursor.fetchall()

    @staticmethod
    def get_by_id(person_id: int) -> Optional[tuple]:
        """
        Retorna um entregador específico pelo ID.

        Args:
            person_id (int): ID do entregador.

        Returns:
            Optional[tuple]: Dados do entregador.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM delivery_person WHERE id = ?;", (person_id,))
            return cursor.fetchone()

    @staticmethod
    def update(
        person_id: int,
        name: Optional[str] = None,
        cpf: Optional[str] = None,
        user_id: Optional[int] = None,
        birth_date: Optional[str] = None,
        celphone: Optional[str] = None
    ) -> None:
        """
        Atualiza os dados de um entregador no banco de dados.

        Args:
            person_id (int): ID do entregador.
            name (Optional[str]): Novo nome.
            cpf (Optional[str]): Novo CPF.
            user_id (Optional[int]): ID do novo usuário.
            birth_date (Optional[str]): Nova data de nascimento.
            celphone (Optional[str]): Novo telefone.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            fields, values = [], []

            if name:
                fields.append("name = ?")
                values.append(name)
            if cpf:
                fields.append("cpf = ?")
                values.append(cpf)
            if user_id:
                fields.append("user_id = ?")
                values.append(user_id)
            if birth_date:
                fields.append("birth_date = ?")
                values.append(birth_date)
            if celphone:
                fields.append("celphone = ?")
                values.append(celphone)
            if not fields:
                return

            values.append(person_id)
            query = f"UPDATE delivery_person SET {', '.join(fields)} WHERE id = ?;"
            cursor.execute(query, values)
            conn.commit()

    @staticmethod
    def delete(person_id: int) -> None:
        """
        Remove um entregador do banco de dados.

        Args:
            person_id (int): ID do entregador a ser removido.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM delivery_person WHERE id = ?;", (person_id,))
            conn.commit()
