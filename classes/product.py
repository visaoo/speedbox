from db.database import get_connection

class Product:
    def __init__(self, name:str, description:str, weight:float, size:float):
        self._name = name
        self._description = description
        self._weight = weight
        self._size = size
        

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        self._weight = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def insert(self) -> None:
        """
        Insere o veículo no banco de dados com o delivery_person_id.

        Args:
            delivery_person_id (int): ID do entregador associado ao veículo.
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO produto (name, descricao, peso, tamanho)
                VALUES (?, ?, ?, ?);
            """, (self.name, self.description, self.weight, self.size))
            conn.commit()



    def __str__(self):
        return (f'Produto:{self.name};'
                f'Descrição:{self.description}'
                f'Peso: {self.weight}'
                f'Tamanho:{self.size}')
    
    def to_dict(self):
        return{
            'Nome': self.name,
            'Descricao': self.description,
            'Peso': self.weight,
            'Tamanho': self.size
        }