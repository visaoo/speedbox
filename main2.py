import re
import sqlite3
from datetime import datetime
from enum import Enum

from classes.address.address import Address
from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService
from classes.order import Order
from classes.user.client import Client
from classes.user.delivery_person import DeliveryPerson
from classes.user.enterprise import Enterprise
from classes.user.user import User
from classes.Vehicle import Vehicle, VehicleType


# Enum para MaxDistance
class MaxDistance:
    MUNICIPAL = "municipal"
    ESTADUAL = "estadual"
    INTER_ESTADUAL = "inter_estadual"


# Enum para OrderStatus (alinhado com o CHECK do banco)
class OrderStatus(Enum):
    PAYMENT_PENDING = "payment_pending"
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELED = "canceled"


# Função auxiliar para conexão com o banco
def get_connection():
    conn = sqlite3.connect("database.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# Funções de validação
def validate_cpf(cpf):
    return bool(re.match(r"^\d{11}$", cpf))


def validate_cnpj(cnpj):
    return bool(re.match(r"^\d{14}$", cnpj))


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_address_from_input(type_user, client_id=None, enterprise_id=None):
    while True:
        street = input("Digite a rua: ").strip()
        if not street:
            print("Rua não pode ser vazia!")
            continue
        number = input("Digite o número: ").strip()
        if not number:
            print("Número não pode ser vazio!")
            continue
        neighborhood = input("Digite o bairro: ").strip()
        if not neighborhood and type_user == "client":
            print("Bairro não pode ser vazio para clientes!")
            continue
        city = input("Digite a cidade: ").strip()
        if not city:
            print("Cidade não pode ser vazia!")
            continue
        state = input("Digite o estado: ").strip()
        if not state:
            print("Estado não pode ser vazio!")
            continue
        try:
            return Address(street, number, neighborhood, city, state, client_id=client_id, enterprise_id=enterprise_id)
        except ValueError as e:
            print(f"Erro: {e}")
            continue


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


# Login
def login(authenticator):
    username = input("Digite o nome de usuário: ").strip()
    password = input("Digite a senha: ").strip()
    user = authenticator.authenticate(username, password)
    if user:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_type FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                return result[0], result[1]
    print("Usuário ou senha inválidos!")
    return None, None


# Funcionalidades do Cliente
def view_order_history_client(client_id):
    orders = Order.get_by_client(client_id)
    if not orders:
        print("Nenhum pedido encontrado.")
        return
    for order in orders:
        print(f"ID: {order[0]}, Total: {order[1]}, Data: {order[2]}, Descrição: {order[3]}, Status: {order[4]}, Origem: {order[5]}, Destino: {order[6]}")


def view_open_orders_client(client_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE client_id = ? AND status IN ('payment_pending', 'pending')", (client_id,))
        orders = cursor.fetchall()
    if not orders:
        print("Nenhum pedido em aberto.")
        return
    for order in orders:
        # print("Pedido em aberto:", order)
        # print(f"ID: {order[0]}, Total: {order[1]}, Data: {order[2]}, Descrição: {order[3]}, Status: {order[4]}, Origem: {order[5]}, Destino: {order[6]}")
        ...


def make_order_client(client_id):
    description = input("Digite a descrição do pedido: ").strip()
    print("Endereço de origem:")
    origem = get_address_from_input("client")
    print("Endereço de destino:")
    destino = get_address_from_input("client")

    order = Order(origem, destino, description, OrderStatus.PENDING)

    # Calcular distância (se API estiver configurada)
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM vehicle WHERE delivery_person_id IS NULL LIMIT 1")
            vehicle_id = cursor.fetchone()
            if vehicle_id:
                vehicle = Vehicle.get_by_id(vehicle_id[0])
                if vehicle:
                    vehicle_obj = Vehicle(
                        model=vehicle[1],
                        mark=vehicle[2],
                        plate=vehicle[3],
                        type_vehicle=VehicleType(vehicle[4]),
                        maximum_distance=vehicle[5]
                    )
                    distance_info = vehicle_obj.calculate_distance(str(origem), str(destino))
                    if distance_info:
                        print(f"Distância: {distance_info['distancia_km']} km, Duração: {distance_info['duracao_horas']} horas")
                        order.value_total = float(distance_info['distancia_km']) * 2.0  # Exemplo de cálculo
    except Exception as e:
        print(f"Erro ao calcular distância: {e}")

    # Inserir pedido com client_id
    order.insert("client", client_id=client_id)
    print("Pedido criado com sucesso!")


# Funcionalidades da Empresa
def view_order_history_enterprise(enterprise_id):
    orders = Order.get_by_enterprise(enterprise_id)
    if not orders:
        print("Nenhum pedido encontrado.")
        return
    for order in orders:
        print(f"ID: {order[0]}, Total: {order[1]}, Data: {order[2]}, Descrição: {order[3]}, Status: {order[4]}, Origem: {order[5]}, Destino: {order[6]}")


def view_open_orders_enterprise(enterprise_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders_enterprises WHERE enterprise_id = ? AND status IN ('payment_pending', 'pending')", (enterprise_id,))
        orders = cursor.fetchall()
    if not orders:
        print("Nenhum pedido em aberto.")
        return
    for order in orders:
        print(f"ID: {order[0]}, Total: {order[1]}, Data: {order[2]}, Descrição: {order[3]}, Status: {order[4]}, Origem: {order[5]}, Destino: {order[6]}")


def make_order_enterprise(enterprise_id):
    description = input("Digite a descrição do pedido: ").strip()
    print("Endereço de origem:")
    origem = get_address_from_input("enterprise")
    print("Endereço de destino:")
    destino = get_address_from_input("enterprise")

    order = Order(origem, destino, description, OrderStatus.PENDING)

    # Calcular distância (se API estiver configurada)
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM vehicle WHERE delivery_person_id IS NULL LIMIT 1")
            vehicle_id = cursor.fetchone()
            if vehicle_id:
                vehicle = Vehicle.get_by_id(vehicle_id[0])
                if vehicle:
                    vehicle_obj = Vehicle(
                        model=vehicle[1],
                        mark=vehicle[2],
                        plate=vehicle[3],
                        type_vehicle=VehicleType(vehicle[4]),
                        maximum_distance=vehicle[5]
                    )
                    distance_info = vehicle_obj.calculate_distance(str(origem), str(destino))
                    if distance_info:
                        print(f"Distância: {distance_info['distancia_km']} km, Duração: {distance_info['duracao_horas']} horas")
                        order.value_total = float(distance_info['distancia_km']) * 2.0  # Exemplo de cálculo
    except Exception as e:
        print(f"Erro ao calcular distância: {e}")

    # Inserir pedido com enterprise_id
    order.insert("enterprise", enterprise_id=enterprise_id)
    print("Pedido criado com sucesso!")


# Funcionalidades do Entregador
def view_orders_delivery_person(delivery_person_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE delivery_person_id = ? OR (status = 'pending' AND delivery_person_id IS NULL)", (delivery_person_id,))
        client_orders = cursor.fetchall()
        cursor.execute("SELECT * FROM orders_enterprises WHERE delivery_person_id = ? OR (status = 'pending' AND delivery_person_id IS NULL)", (delivery_person_id,))
        enterprise_orders = cursor.fetchall()

    if not (client_orders or enterprise_orders):
        print("Nenhum pedido disponível.")
        return
    print("\nPedidos de Clientes:")
    for order in client_orders:
        print(f"ID: {order[0]}, Total: {order[1]}, Data: {order[2]}, Descrição: {order[3]}, Status: {order[4]}, Origem: {order[5]}, Destino: {order[6]}")
    print("\nPedidos de Empresas:")
    for order in enterprise_orders:
        print(f"ID: {order[0]}, Total: {order[1]}, Data: {order[2]}, Descrição: {order[3]}, Status: {order[4]}, Origem: {order[5]}, Destino: {order[6]}")


def accept_order_delivery_person(delivery_person_id):
    order_type = input("Digite o tipo de pedido (client/enterprise): ").strip()
    order_id = input("Digite o ID do pedido: ").strip()
    try:
        order_id = int(order_id)
        Order.update_delivery_person(order_type, order_id, delivery_person_id)
        Order.update_status(order_id, OrderStatus.PENDING, order_type)  # Mantém 'pending' após aceitação
        print("Pedido aceito com sucesso!")
    except ValueError:
        print("ID do pedido deve ser um número!")
    except Exception as e:
        print(f"Erro ao aceitar pedido: {e}")


def update_order_status_delivery_person(delivery_person_id):
    order_type = input("Digite o tipo de pedido (client/enterprise): ").strip()
    order_id = input("Digite o ID do pedido: ").strip()
    new_status = input("Digite o novo status (completed/canceled): ").strip()
    try:
        order_id = int(order_id)
        new_status = OrderStatus[new_status.upper()]
        with get_connection() as conn:
            cursor = conn.cursor()
            table = "orders" if order_type == "client" else "orders_enterprises"
            cursor.execute(f"SELECT delivery_person_id FROM {table} WHERE id = ?", (order_id,))
            result = cursor.fetchone()
            if result and result[0] == delivery_person_id:
                Order.update_status(order_id, new_status, order_type)
                print("Status atualizado com sucesso!")
            else:
                print("Erro: Você não é o entregador responsável por este pedido ou o pedido não existe.")
    except KeyError:
        print("Status inválido! Use 'completed' ou 'canceled'.")
    except ValueError:
        print("ID do pedido inválido!")
    except Exception as e:
        print(f"Erro ao atualizar status: {e}")


# Menus
def client_menu(client_id):
    while True:
        print("\n=== Menu do Cliente ===")
        print("1. Visualizar histórico de pedidos")
        print("2. Fazer um pedido")
        print("3. Ver pedidos em aberto")
        print("4. Sair")
        choice = input("Escolha uma opção: ").strip()
        if choice == "1":
            view_order_history_client(client_id)
        elif choice == "2":
            make_order_client(client_id)
        elif choice == "3":
            view_open_orders_client(client_id)
        elif choice == "4":
            break
        else:
            print("Opção inválida!")


def enterprise_menu(enterprise_id):
    while True:
        print("\n=== Menu da Empresa ===")
        print("1. Visualizar histórico de pedidos")
        print("2. Fazer um pedido")
        print("3. Ver pedidos em aberto")
        print("4. Sair")
        choice = input("Escolha uma opção: ").strip()
        if choice == "1":
            view_order_history_enterprise(enterprise_id)
        elif choice == "2":
            make_order_enterprise(enterprise_id)
        elif choice == "3":
            view_open_orders_enterprise(enterprise_id)
        elif choice == "4":
            break
        else:
            print("Opção inválida!")


def delivery_person_menu(delivery_person_id):
    while True:
        print("\n=== Menu do Entregador ===")
        print("1. Visualizar pedidos disponíveis")
        print("2. Aceitar um pedido")
        print("3. Alterar status de um pedido")
        print("4. Sair")
        choice = input("Escolha uma opção: ").strip()
        if choice == "1":
            view_orders_delivery_person(delivery_person_id)
        elif choice == "2":
            accept_order_delivery_person(delivery_person_id)
        elif choice == "3":
            update_order_status_delivery_person(delivery_person_id)
        elif choice == "4":
            break
        else:
            print("Opção inválida!")


# Menu principal
def main():
    authenticator = Authenticator(AuthService(db_path="database.db"))
    while True:
        print("\n=== Sistema de Delivery ===")
        print("1. Login")
        print("2. Cadastrar Cliente")
        print("3. Cadastrar Entregador")
        print("4. Cadastrar Empresa")
        print("5. Sair")
        choice = input("Escolha uma opção: ").strip()
        if choice == "1":
            user_id, user_type = login(authenticator)
            if user_id:
                # Obter o ID correto com base no tipo de usuário
                with get_connection() as conn:
                    cursor = conn.cursor()
                    if user_type == "client":
                        cursor.execute("SELECT id FROM clients WHERE user_id = ?", (user_id,))
                        entity_id = cursor.fetchone()
                        if entity_id:
                            client_menu(entity_id[0])
                        else:
                            print("Erro: Cliente não encontrado.")
                    elif user_type == "delivery_person":
                        cursor.execute("SELECT id FROM delivery_person WHERE user_id = ?", (user_id,))
                        entity_id = cursor.fetchone()
                        if entity_id:
                            delivery_person_menu(entity_id[0])
                        else:
                            print("Erro: Entregador não encontrado.")
                    elif user_type == "enterprise":
                        cursor.execute("SELECT id FROM enterprises WHERE user_id = ?", (user_id,))
                        entity_id = cursor.fetchone()
                        if entity_id:
                            enterprise_menu(entity_id[0])
                        else:
                            print("Erro: Empresa não encontrado.")
        elif choice == "2":
            register_user(authenticator, "client")
        elif choice == "3":
            register_user(authenticator, "delivery_person")
        elif choice == "4":
            register_user(authenticator, "enterprise")
        elif choice == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()
