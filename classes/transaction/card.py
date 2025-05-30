import sqlite3
from datetime import datetime
from enum import Enum


class CardFlag(Enum):
    VISA = 'Visa'
    MASTERCARD = 'Mastercard'
    DINERS = 'Diners Club'
    DISCOVER = 'Discover'
    JCB = 'JCB'
    AMERICAN_EXPRESS = 'American Express'
    MASTERCARD_BIN = 'Mastercard BIN'
    UNIDENTIFIED = 'Unidentified'


class Card:
    def __init__(self, name: str, number: str, validity: str, cvc: str) -> None:
        """Inicializa um objeto Card com nome, número, validade, CVC e bandeira."""
        self._name: str = name
        self._number: str = self._clean_number(number)
        self._validity: str = validity
        self._cvc: str = cvc
        self._flag: CardFlag = self.identify_flag()

    @property
    def name(self) -> str:
        """Retorna o nome do titular do cartão."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Define o nome do titular do cartão."""
        self._name = value

    @property
    def number(self) -> str:
        """Retorna o número do cartão (sem espaços ou hífens)."""
        return self._number

    @number.setter
    def number(self, value: str) -> None:
        """Define o número do cartão e atualiza a bandeira."""
        self._number = self._clean_number(value)
        self._flag = self.identify_flag()

    @staticmethod
    def _clean_number(number: str) -> str:
        """Remove espaços e hífens do número do cartão e valida.

        Args:
            number (str): Número do cartão.

        Retorna:
            str: Número limpo com apenas dígitos.

        Lança:
            ValueError: Se o número for inválido.
        """
        cleaned: str = ''.join(c for c in number if c.isdigit())
        if not cleaned.isdigit():
            raise ValueError("O número deve conter apenas dígitos")
        if len(cleaned) < 13 or len(cleaned) > 19:
            raise ValueError("O número deve ter entre 13 e 19 dígitos")
        return cleaned

    @property
    def validity(self) -> str:
        """Retorna a data de validade do cartão no formato MM/AA ou MM/AAAA."""
        return self._validity

    @validity.setter
    def validity(self, value: str) -> None:
        """Define a validade do cartão após validação.

        Args:
            value (str): Validade no formato MM/AA ou MM/AAAA.

        Lança:
            ValueError: Se a data for inválida ou o cartão estiver expirado.
        """
        try:
            month_str, year_str = value.split("/")
            month: int = int(month_str)
            year: int = int(year_str) if len(year_str) == 4 else int(f"20{year_str}")

            if month < 1 or month > 12:
                raise ValueError("Mês inválido")

            now = datetime.now()
            if year > now.year or (year == now.year and month >= now.month):
                self._validity = value
            else:
                raise ValueError("Cartão expirado")
        except Exception as e:
            raise ValueError(f"Data de validade inválida: {e}")

    @property
    def cvc(self) -> str:
        """Retorna o código de segurança do cartão (CVC)."""
        return self._cvc

    @cvc.setter
    def cvc(self, value: str) -> None:
        """Define o código de segurança do cartão.

        Args:
            value (str): CVC com 3 ou 4 dígitos.

        Lança:
            ValueError: Se o CVC for inválido.
        """
        if not value.isdigit() or len(value) not in {3, 4}:
            raise ValueError("CVC deve ter 3 ou 4 dígitos")
        self._cvc = value

    @property
    def flag(self) -> CardFlag:
        """Retorna a bandeira do cartão."""
        return self._flag

    def identify_flag(self) -> CardFlag:
        """Identifica a bandeira do cartão com base no número.

        Retorna:
            CardFlag: Enum representando a bandeira identificada.
        """
        num: str = self._number

        if num.startswith('4') and len(num) in {13, 16}:
            return CardFlag.VISA

        if ((len(num) == 16) and
            ((num.startswith(('51', '52', '53', '54', '55')) or
             (num.startswith('22') and 221 <= int(num[:3]) <= 272) or
             (num.startswith('2') and 2210 <= int(num[:4]) <= 2720)))):
            return CardFlag.MASTERCARD

        if num.startswith(('34', '37')) and len(num) == 15:
            return CardFlag.AMERICAN_EXPRESS

        diners_prefixes = ('300', '301', '302', '303', '304', '305', '36', '38', '39')
        if any(num.startswith(p) for p in diners_prefixes) and len(num) in {14, 15, 16}:
            return CardFlag.DINERS

        if ((len(num) == 16) and
            (num.startswith('6011') or
             num.startswith(('644', '645', '646', '647', '648', '649')) or
             num.startswith('65'))):
            return CardFlag.DISCOVER

        if (num.startswith('35') and
            len(num) in {16, 17, 18, 19} and
            3528 <= int(num[:4]) <= 3589):
            return CardFlag.JCB

        if num.startswith('22') and len(num) == 16:
            return CardFlag.MASTERCARD_BIN

        return CardFlag.UNIDENTIFIED

    def insert(self) -> None:
        """Insere os dados do cartão no banco de dados."""
        with sqlite3.connect("speedbox.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO card (name, number, validity, cvc, flag)
                VALUES (?, ?, ?, ?, ?);
            """, (self.name, self.number, self.validity, self.cvc, self.flag.value))
            conn.commit()

    @staticmethod
    def get_by_transaction(transaction_id: str) -> tuple | None:
        """Busca um cartão vinculado a uma transação.

        Args:
            transaction_id (str): ID da transação.

        Retorna:
            tuple | None: Tupla com os dados do cartão ou None.
        """
        with sqlite3.connect("speedbox.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM card WHERE transaction_id = ?;", (transaction_id,))
            return cursor.fetchone()

    @staticmethod
    def delete_by_transaction(transaction_id: str) -> None:
        """Remove o cartão vinculado a uma transação do banco de dados.

        Args:
            transaction_id (str): ID da transação.
        """
        with sqlite3.connect("speedbox.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM card WHERE transaction_id = ?;", (transaction_id,))
            conn.commit()

    def to_dict(self) -> dict:
        """Retorna os dados do cartão em formato de dicionário.

        Retorna:
            dict: Dados do cartão.
        """
        return {
            "name": self.name,
            "number": self.number,
            "validity": self.validity,
            "cvc": self.cvc,
            "flag": self.flag.value
        }

    def __str__(self) -> str:
        """Retorna uma representação textual do cartão.

        Retorna:
            str: Dados formatados do cartão.
        """
        return f"Card(name={self.name}, number={self.number}, validity={self.validity}, cvc={self.cvc}, flag={self.flag.value})"
