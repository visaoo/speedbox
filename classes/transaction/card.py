from enum import Enum
from datetime import datetime
from typing import Optional
from classes.transaction.transaction import Transaction

class CardFlag(Enum):
    VISA = 'Visa'
    MASTERCARD = 'Mastercard'
    DINERS = 'Diners Club'
    DISCOVER = 'Discover'
    JCB = 'JCB'
    AMERICAN_EXPRESS = 'American Express'
    MASTERCARD_BIN = 'Mastercard BIN'
    UNIDENTIFIED = 'Unidentified'

class Card(Transaction):
    def __init__(self, name: str, number: str, validity: str, cvc: str):
        super().__init__(value_total=0.0, payment_method='card', status='pending')
        self._name = name
        self._number = self._clean_number(number)
        self._validity = validity
        self._cvc = cvc
        self._flag = self.identify_flag()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def number(self) -> str:
        return self._number

    @number.setter
    def number(self, value: str) -> None:
        self._number = self._clean_number(value)
        self._flag = self.identify_flag()

    @staticmethod
    def _clean_number(number: str) -> str:
        """Remove espaços e hífens do número do cartão e valida."""
        cleaned = ''.join(c for c in number if c.isdigit())
        if not cleaned.isdigit():
            raise ValueError("O número deve conter apenas dígitos")
        if len(cleaned) < 13 or len(cleaned) > 19:  # Cartões podem ter até 19 dígitos
            raise ValueError("O número deve ter entre 13 e 19 dígitos")
        return cleaned

    @property
    def validity(self) -> str:
        return self._validity

    @validity.setter
    def validity(self, value: str) -> None:
        try:
            month_str, year_str = value.split("/")
            month = int(month_str)
            year = int(year_str) if len(year_str) == 4 else int(f"20{year_str}")
            
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
        return self._cvc

    @cvc.setter
    def cvc(self, value: str) -> None:
        if not value.isdigit() or len(value) not in {3, 4}:
            raise ValueError("CVC deve ter 3 ou 4 dígitos")
        self._cvc = value

    @property
    def flag(self) -> CardFlag:
        return self._flag

    def identify_flag(self) -> CardFlag:
        """Identifica a bandeira do cartão com base no número."""
        num = self._number
        
        # Visa: 4, 13 ou 16 dígitos
        if num.startswith('4') and len(num) in {13, 16}:
            return CardFlag.VISA
            
        # Mastercard: 51-55, 2221-2720, 16 dígitos
        if ((len(num) == 16) and 
            ((num.startswith(('51', '52', '53', '54', '55')) or
             (num.startswith('22') and 221 <= int(num[:3]) <= 272) or
             (num.startswith('2') and 2210 <= int(num[:4]) <= 2720)))):
            return CardFlag.MASTERCARD
            
        # American Express: 34 ou 37, 15 dígitos
        if num.startswith(('34', '37')) and len(num) == 15:
            return CardFlag.AMERICAN_EXPRESS
            
        # Diners Club: múltiplos prefixos, 14-16 dígitos
        diners_prefixes = (
            '300', '301', '302', '303', '304', '305', '36', '38', '39'
        )
        if (any(num.startswith(p) for p in diners_prefixes) and 
            len(num) in {14, 15, 16}):
            return CardFlag.DINERS
            
        # Discover: 6011, 644-649, 65, 16 dígitos
        if ((len(num) == 16) and 
            (num.startswith('6011') or 
             num.startswith(('644', '645', '646', '647', '648', '649')) or
             num.startswith('65'))):
            return CardFlag.DISCOVER
            
        # JCB: 3528-3589, 16-19 dígitos
        if (num.startswith('35') and 
            len(num) in {16, 17, 18, 19} and
            3528 <= int(num[:4]) <= 3589):
            return CardFlag.JCB
            
        # Mastercard BIN: 22, 16 dígitos (caso especial)
        if num.startswith('22') and len(num) == 16:
            return CardFlag.MASTERCARD_BIN
            
        return CardFlag.UNIDENTIFIED