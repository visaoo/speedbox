from dataclasses import dataclass
from random import randint
from datetime import datetime, timedelta

import sqlite3

import sqlite3
from datetime import datetime, timedelta
from random import randint

class Boleto:
    def __init__(self) -> None:
        """Inicializa um objeto Boleto com data de vencimento e linha digitável."""
        self.due_date: str = self.generate_due_date()
        self.typeline: str = self.generate_typeline()

    def generate_due_date(self) -> str:
        """Gera a data de vencimento do boleto.

        Retorna:
            str: Data de vencimento formatada no padrão "dd/mm/yyyy".
        """
        due_date: datetime = datetime.now() + timedelta(days=3)
        return due_date.strftime("%d/%m/%Y")
    
    def generate_typeline(self) -> str:
        """Gera a linha digitável do boleto.

        Retorna:
            str: Linha digitável composta por 47 dígitos aleatórios.
        """
        return ''.join(str(randint(0, 9)) for _ in range(47))
    
    def insert(self) -> None:
        """Insere o boleto no banco de dados.
        
        A tabela 'boleto' deve possuir as colunas: due_date, typeline.
        """
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO boleto (due_date, typeline)
                VALUES (?, ?);
            """, (self.due_date, self.typeline))
            conn.commit()
            
    @staticmethod
    def get_by_transaction(transaction_id: str) -> tuple | None:
        """Obtém um boleto associado a uma transação específica.

        Args:
            transaction_id (str): ID da transação associada ao boleto.

        Retorna:
            tuple | None: Dados do boleto encontrado ou None se não houver resultado.
        """
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM boleto WHERE transaction_id = ?;", (transaction_id,))
            return cursor.fetchone()
        
    @staticmethod
    def delete_by_transaction(transaction_id: str) -> None:
        """Remove um boleto associado a uma transação específica do banco de dados.

        Args:
            transaction_id (str): ID da transação associada ao boleto.
        """
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM boleto WHERE transaction_id = ?;", (transaction_id,))
            conn.commit()

    def to_dict(self) -> dict:
        """Retorna uma representação do boleto em formato de dicionário.

        Retorna:
            dict: Dicionário com os campos due_date e typeline.
        """
        return {
            "due_date": self.due_date,
            "typeline": self.typeline
        }
    
    def __str__(self) -> str:
        """Retorna a representação textual do objeto Boleto.

        Retorna:
            str: String formatada com os dados do boleto.
        """
        return f"Boleto(due_date={self.due_date}, typeline={self.typeline})"
