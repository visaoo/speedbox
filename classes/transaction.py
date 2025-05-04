from abc import ABC, abstractmethod
from enum import Enum
from uuid import uuid4

class Transaction(ABC):
    def __init__(self, value, date, time_for_pay, payment_status):
        self._value
        self._date
        self._time_for_pay
        self._payment_status
        

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

    @abstractmethod
    def make_payment(self):
        pass
    
    @abstractmethod
    def cancel_payment(self):
        pass
    
    @abstractmethod
    def update_status():
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
        self._number = value

    @property
    def validity(self):
        return self._validity

    @validity.setter
    def validity(self, value):
        self._validity = value

    @property
    def cvc(self):
        return self._cvc

    @cvc.setter
    def cvc(self, value):
        self._cvc = value

    @property
    def flag(self):
        return self._flag

    @flag.setter
    def flag(self, value):
        self._flag = value


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

class Type_Key_Pix(Enum):
    EMAIL = 'email'
    UUID = uuid4()
    CELPHONE = 'celphone'
    CPF = 'CPF'
    CNPJ = 'cnpj'


class Pix(Transaction):
    def __init__(self, value, date, time_for_pay, payment_status, key, key_type):
        super().__init__(value, date, time_for_pay, payment_status)
        self._key = key
        self._key_type = key_type


    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        self._key = value

    @property
    def key_type(self):
        return self._key_type

    @key_type.setter
    def key_type(self, value):
        self._key_type = value

