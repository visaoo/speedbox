from dataclasses import dataclass
from random import randint
from datetime import datetime, timedelta


@dataclass
class Boleto:
    def __init__(self):
        self.due_date = self.generate_due_date()
        self.typeline = self.generate_typeline()

    def generate_due_date(self):
        due_date =  datetime.now() + timedelta(days=3)
        return due_date.strftime("%d/%m/%Y")
    
    def generate_typeline():
        return ''.join(str(randint(0, 9)) for _ in range(47))
    
    
    def to_dict(self):
        return {
            "due_date": self.due_date,
            "typeline": self.typeline
        }
    
    def __str__(self):
        return f"Boleto(due_date={self.due_date}, typeline={self.typeline})"