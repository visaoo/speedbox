from abc import ABC, abstractmethod
from enum import Enum
from uuid import uuid4
from datetime import datetime
import qrcode
from Address import Address
from client import Client
from enterprise import Enterprise


class Transaction(ABC):
    def __init__(self, value, date, time_for_pay, payment_status):
        self._value = value
        self._date = date
        self._time_for_pay = time_for_pay
        self._payment_status = payment_status
        # self._client = client
        # self._enterprise = enterprise

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def time_for_pay(self):
        return self._time_for_pay

    @time_for_pay.setter
    def time_for_pay(self, value):
        self._time_for_pay = value

    @property
    def payment_status(self):
        return self._payment_status

    @payment_status.setter
    def payment_status(self, value):
        self._payment_status = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    @property
    def enterprise(self):
        return self._enterprise

    @enterprise.setter
    def enterprise(self, value):
        self._enterprise = value


    @abstractmethod
    def make_payment(self):
        pass
    
    @abstractmethod
    def cancel_payment(self):
        pass
    
    @abstractmethod
    def update_status(self):
        pass

class Card(Transaction):
    def __init__(self, value, date, time_for_pay, payment_status, name, number, validity, cvc, flag):
        super().__init__(value, date, time_for_pay, payment_status)
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
        if len(cleaned_value) < 13 or len(cleaned_value) > 19:
            raise ValueError("O número deve ter entre 13 e 19 dígitos")
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
        if value.isdigit() and len(value) in [3,4]:
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
            self.flag = "Mastercard (novos binários)"
            return 
        else:
            return "Bandeira não identificada"



class Boleto(Transaction):
    def __init__(self, value, date, time_for_pay, payment_status, code_bar, typeable_line):
        super().__init__(value, date, time_for_pay, payment_status)
        self._code_bar = code_bar
        self._typeable_line = typeable_line


    @property
    def code_bar(self):
        return self._code_bar

    @code_bar.setter
    def code_bar(self, value):
        self._code_bar = value

    @property
    def typeable_line(self):
        return self._typeable_line

    @typeable_line.setter
    def typeable_line(self, value):
        self._typeable_line = value



