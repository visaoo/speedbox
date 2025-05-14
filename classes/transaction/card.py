from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship
from db.database import Base


class Card(Base):
    __tablename__ = 'card'

    transaction_id = Column(Integer, ForeignKey('transactions.id'), primary_key=True)
    number_card = Column(String(16))
    flag = Column(String(20))
    atorization_status = Column(String(20))

    transaction = relationship('Trasaction', back_populates='card')

    def __init__(self, name, number, validity, cvc, flag):
        self._name = name
        self._number = number
        self._validity = validity
        self._cvc = cvc
        self._flag = flag

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        cleaned_value = str(value).replace(' ', '').replace('-', '')
        if not cleaned_value.isdigit():
            raise ValueError("O número deve conter apenas dígitos")
        if len(cleaned_value) < 13 or len(cleaned_value) > 16:
            raise ValueError("O número deve ter entre 13 e 16 dígitos")
        self._number = cleaned_value

    @property
    def validity(self):
        return self._validity

    @validity.setter
    def validity(self, value):
        try:
            exp_month, exp_year = self._validity.split("/")
            exp_month = int(exp_month)
            exp_year = int("20" + exp_year) if len(exp_year) == 2 else int(exp_year)
            now = datetime.now()
            if exp_year > now.year or (exp_year == now.year and exp_month >= now.month):
                self._validity = value
        except Exception as e:
            print(f'ERRO [{e}]')

    @property
    def cvc(self):
        return self._cvc

    @cvc.setter
    def cvc(self, value):
        if value.isdigit() and len(value) in [3, 4]:
            self._cvc = value
        raise ValueError('CVC diferente de 3')

    @property
    def flag(self):
        return self._flag

    def identificar_bandeira(self):

        # Identificação por prefixo e comprimento
        if (self.number.startswith('4') and
            len(self.number) in [13, 16]):
            self.flag = "Visa"
            return
        elif ((self.number.startswith('51') or
            self.number.startswith('52') or
            self.number.startswith('53') or
            self.number.startswith('54') or
            self.number.startswith('55')) and
            len(self.number) == 16):
            self.flag = "Mastercard"
            return
        elif ((self.number.startswith('34') or
            self.number.startswith('37')) and
            len(self.number) == 15):
            self.flag = "American Express"
            return
        elif ((self.number.startswith('300') or
            self.number.startswith('301') or
            self.number.startswith('302') or
            self.number.startswith('303') or
            self.number.startswith('304') or
            self.number.startswith('305') or
            self.number.startswith('36') or
            self.number.startswith('38') or
            self.number.startswith('39')) and
            len(self.number) in [14, 15, 16]):
            self.flag = "Diners Club"
            return
        elif (self.number.startswith('6011') and
            len(self.number) == 16):
            self.flag = "Discover"
            return
        elif ((self.number.startswith('35') and
            len(self.number) in [16, 17, 18, 19])):
            self.flag = "JCB"
            return
        elif ((self.number.startswith('22') and
            len(self.number) in [16])):
            self.flag = "Mastercard BIN"
            return
        else:
            return "Bandeira não identificada"
