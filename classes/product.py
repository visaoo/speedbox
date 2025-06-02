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

    def insert(self, tipo_user:str, order_id:int) -> None:
        """
        Insere o produto no banco de dados com o order_id.

        Args:
            tipo_user(str): tipo de usuario para salvar no banco.
            order_id(int): id do pedido para salvar no banco.
        """
        try:
            with get_connection() as conn:
                if tipo_user == 'client':
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO produto_client (nome, descricao, peso, tamanho, order_id)
                            VALUES (?, ?, ?, ?);
                        """, (order_id, self.name, self.description, self.weight, self.size))
                elif tipo_user == 'enterprise':
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO produto_enterpise (nome, descricao, peso, tamanho, order_id)
                        VALUES (?, ?, ?, ?);
                    """, (order_id, self.name, self.description, self.weight, self.size))
                else:
                    raise 
                conn.commit()
        except Exception as e:
            print(f'Erro: [{e}]')
        
        
        
        
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