from app.utils.get_connection import get_connection
from app.utils.validate_cpf import validate_cpf
from app.utils.validate_date import validate_date
from app.utils.validate_cnpj import validate_cnpj
from app.utils.get_address_from_input import get_address_from_input
from app.utils.max_distance import MaxDistance

from classes.user.client import Client
from classes.user.delivery_person import DeliveryPerson
from classes.user.user import User
from classes.Vehicle import Vehicle, VehicleType
from classes.user.enterprise import Enterprise


# Cadastro de usuários
def register_user(authenticator, user_type):
    print(f"\n=== Cadastro de {user_type} ===")
    username = input("Digite o nome de usuário: ").strip()
    email = input("Digite o email: ").strip()
    password = input("Digite a senha: ").strip()

    # Verificar se usuário já existe
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            print("Erro: Nome de usuário ou email já existe!")
            return

    # Registrar usuário na tabela users
    if not authenticator.register(username, email, password, user_type):
        print("Erro ao cadastrar usuário!")
        return

    # Obter o user_id recém-criado
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        user_id = cursor.fetchone()[0]

    if user_type == "client":
        name = input("Digite o nome: ").strip()
        cpf = input("Digite o CPF (11 dígitos): ").strip()
        if not validate_cpf(cpf):
            print("CPF inválido!")
            return
        birth_date = input("Digite a data de nascimento (YYYY-MM-DD): ").strip()
        if not validate_date(birth_date):
            print("Data inválida!")
            return
        phone = input("Digite o telefone: ").strip()
        address = get_address_from_input("client")
        
        client = Client(name, cpf, phone, birth_date, address, user_id)
        client.insert()
        
        # Obter o client_id recém-criado
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM clients WHERE cpf = ? AND user_id = ?", (cpf, user_id))
            client_id = cursor.fetchone()
            if not client_id:
                print("Erro: Não foi possível recuperar o ID do cliente!")
                return
            client_id = client_id[0]
        
        # Inserir endereço com o client_id correto
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO addresses_clients (street, number, neighborhood, city, state, client_id)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (address.street, address.number, address.neighborhood, address.city, address.state, client_id))
            conn.commit()
        print("Cliente cadastrado com sucesso!")

    elif user_type == "delivery_person":
        name = input("Digite o nome: ").strip()
        cpf = input("Digite o CPF (11 dígitos): ").strip()
        if not validate_cpf(cpf):
            print("CPF inválido!")
            return
        cnh = input("Digite a CNH: ").strip()
        birth_date = input("Digite a data de nascimento (YYYY-MM-DD): ").strip()
        if not validate_date(birth_date):
            print("Data inválida!")
            return
        phone = input("Digite o telefone: ").strip()
        address = get_address_from_input("client")
        
        # Criar entregador primeiro
        delivery_person = DeliveryPerson(name, cpf, birth_date, cnh, True, None, User(username, email, password, user_type), phone, address, user_id)
        delivery_person.insert()
        
        # Obter o delivery_person_id recém-criado
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM delivery_person WHERE cpf = ? AND user_id = ?", (cpf, user_id))
            delivery_person_id = cursor.fetchone()
            if not delivery_person_id:
                print("Erro: Não foi possível recuperar o ID do entregador!")
                return
            delivery_person_id = delivery_person_id[0]
        
        # Cadastro de veículo com delivery_person_id
        model = input("Digite o modelo do veículo: ").strip()
        mark = input("Digite a marca do veículo: ").strip()
        plate = input("Digite a placa do veículo (7 caracteres): ").strip()
        type_vehicle = input("Digite o tipo de veículo (moto/carro/caminhao): ").strip()
        if type_vehicle not in [VehicleType.MOTO.value, VehicleType.CARRO.value, VehicleType.CAMINHAO.value]:
            print("Tipo de veículo inválido!")
            return
        type_vehicle = VehicleType(type_vehicle)
        max_distance = input("Digite a distância máxima (municipal/estadual/inter_estadual): ").strip()
        if max_distance not in [MaxDistance.MUNICIPAL, MaxDistance.ESTADUAL, MaxDistance.INTER_ESTADUAL]:
            print("Distância máxima inválida!")
            return
        
        vehicle = Vehicle(model, mark, plate, type_vehicle, max_distance)
        vehicle.insert(delivery_person_id=delivery_person_id)
        
        # Inserir endereço com o delivery_person_id como client_id
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO addresses_clients (street, number, neighborhood, city, state, client_id)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (address.street, address.number, address.neighborhood, address.city, address.state, delivery_person_id))
            conn.commit()
        
        print("Entregador cadastrado com sucesso!")

    elif user_type == "enterprise":
        name = input("Digite o nome da empresa: ").strip()
        cnpj = input("Digite o CNPJ (14 dígitos): ").strip()
        if not validate_cnpj(cnpj):
            print("CNPJ inválido!")
            return
        address = get_address_from_input("enterprise")
        
        enterprise = Enterprise(name, cnpj, address, user_id)
        enterprise.insert()
        
        # Obter o enterprise_id recém-criado
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM enterprises WHERE cnpj = ? AND user_id = ?", (cnpj, user_id))
            enterprise_id = cursor.fetchone()
            if not enterprise_id:
                print("Erro: Não foi possível recuperar o ID da empresa!")
                return
            enterprise_id = enterprise_id[0]
        
        # Inserir endereço com o enterprise_id correto
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO addresses_enterprises (street, number, neighborhood, city, state, enterprise_id)
                VALUES (?, ?, ?, ?, ?, ?);
            """, (address.street, address.number, address.neighborhood, address.city, address.state, enterprise_id))
            conn.commit()
        
        print("Empresa cadastrada com sucesso!")
