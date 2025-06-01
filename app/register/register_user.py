from app.utils.get_address_from_input import get_address_from_input
from app.utils.get_connection import get_connection
from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService
from classes.colors import Colors
from classes.user.client import Client
from classes.user.delivery_person import DeliveryPerson
from classes.user.enterprise import Enterprise
from classes.Vehicle import MaxDistance, Vehicle, VehicleType
from validations.validations import *


def register_user(user_type):
    auth = Authenticator(AuthService())
    print(f"\n{Colors.BOLD}CADASTRO DE {user_type.upper()} {Colors.ENDC}")

    username = get_input(f"{Colors.CYAN}Nome de usuário: {Colors.ENDC}", none_word).strip()
    email = get_input(f"{Colors.CYAN}Email: {Colors.ENDC}", is_email).strip()
    password = get_input(f"{Colors.CYAN}Senha: {Colors.ENDC}",).strip()

    registered = auth.is_user_registered(username, email)
    if registered:
        print(f"\n{Colors.RED}Erro: Nome de usuário ou email já existe!{Colors.RED}")
        input(f"{Colors.YELLOW}Pressione Enter para tentar novamente...{Colors.ENDC}")
        return

    # Registrar usuário na tabela users
    auth.register(username, email, password, user_type)

    # Obter o user_id recém-criado
    find_user = auth.find_user_by_username(username)
    
    if not find_user:
        print(f"{Colors.RED}Erro: Não foi possível recuperar o ID do usuário!{Colors.RED}")
        return
    
    user_id = find_user.id

    if user_type == "client":
        print(f"\n{Colors.BOLD}INFORMAÇÕES PESSOAIS{Colors.ENDC}")
        name = get_input(f"{Colors.CYAN}Nome completo: {Colors.ENDC}").strip()
        cpf = get_input(f"{Colors.CYAN}CPF (123.456.789-09): {Colors.ENDC}", is_cpf, errorMensage=f"{Colors.RED}CPF inválido. Tente novamente.{Colors.ENDC}").strip()
        birth_date = get_input(f"{Colors.CYAN}Data de nascimento (DD/MM/YYYY): {Colors.ENDC}", is_date, errorMensage=f"{Colors.RED}Data de nascimento inválida (formato DD/MM/YYYY). Tente novamente.{Colors.ENDC}").strip()
        phone = get_input(f"{Colors.CYAN}TELEFONE (11987654321): {Colors.ENDC}", is_phone, errorMensage=f"{Colors.RED}Telefone inválido. Tente novamente.{Colors.ENDC}").strip()
        address = get_address_from_input("client")

        client = Client(name, cpf, phone, birth_date, address, user_id)
        client.insert()

        # Obter o client_id recém-criado
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM clients WHERE cpf = ? AND user_id = ?", (cpf, user_id))
            client_id = cursor.fetchone()
            if not client_id:
                print(f"{Colors.RED}Erro: Não foi possível recuperar o ID do cliente!{Colors.RED}")
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
        print(f"\n{Colors.GREEN}Cliente {name} cadastrado com sucesso!{Colors.ENDC}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")

    elif user_type == "delivery_person":
        print(f"\n{Colors.BOLD}INFORMAÇÕES PESSOAIS{Colors.ENDC}")
        name = get_input(f"{Colors.CYAN}Nome completo: {Colors.ENDC}").strip()
        cpf = get_input(f"{Colors.CYAN}CPF (123.456.789-09): {Colors.ENDC}", is_cpf, errorMensage=f"{Colors.RED}CPF inválido. Tente novamente.{Colors.ENDC}").strip()
        cnh = get_input(f"{Colors.CYAN}CNH: {Colors.ENDC}", is_cnh, errorMensage=f"{Colors.RED}CNH inválida. Tente novamente.{Colors.ENDC}").strip()
        birth_date = get_input(f"{Colors.CYAN}Data de nascimento (DD/MM/YYYY): {Colors.ENDC}", is_date, errorMensage=f"{Colors.RED}Data de nascimento inválida (formato DD/MM/YYYY). Tente novamente.{Colors.ENDC}").strip()
        phone = get_input(f"{Colors.CYAN}TELEFONE (11987654321): {Colors.ENDC}", is_phone, errorMensage=f"{Colors.RED}Telefone inválido. Tente novamente.{Colors.ENDC}").strip()
        address = get_address_from_input("delivery_person")

        # Criar entregador primeiro
        delivery_person = DeliveryPerson(name, cpf, birth_date, cnh, True, None, phone=phone, address=address, user_id=user_id)
        delivery_person.insert()

        # Obter o delivery_person_id recém-criado
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM delivery_person WHERE cpf = ? AND user_id = ?", (cpf, user_id))
            delivery_person_id = cursor.fetchone()
            if not delivery_person_id:
                print(f"{Colors.RED}Erro: Não foi possível recuperar o ID do entregador!{Colors.RED}")
                return
            delivery_person_id = delivery_person_id[0]

        # Cadastro de veículo com delivery_person_id

        print(f"\n{Colors.BOLD}INFORMAÇÕES DO VEÍCULO{Colors.ENDC}")
        model = get_input(f"{Colors.CYAN}Modelo do veículo: {Colors.ENDC}", none_word).strip()
        mark = get_input(f"{Colors.CYAN}Marca do veículo: {Colors.ENDC}", none_word).strip()
        plate = get_input(f"{Colors.CYAN}Placa do veículo (formato AAA0000 ou ABC1D23): {Colors.ENDC}", is_valid_plate, errorMensage=f"{Colors.RED}A placa digitada não é válida (formato AAA0000 ou ABC1D23). Tente novamente.{Colors.ENDC}").strip()
        type_vehicle = get_input(f"{Colors.CYAN}Digite o tipo de veículo (moto/carro/caminhao): {Colors.ENDC}", none_word).strip()

        if type_vehicle not in [VehicleType.MOTO.value, VehicleType.CARRO.value, VehicleType.CAMINHAO.value]:
            print(f"{Colors.RED}Tipo de veículo inválido!{Colors.RED}")
            return
        type_vehicle = VehicleType(type_vehicle)
        max_distance = get_input(f"{Colors.CYAN}Digite a distância máxima (municipal/estadual/inter_estadual): {Colors.ENDC}", none_word).strip()

        if max_distance not in [MaxDistance.MUNICIPAL, MaxDistance.ESTADUAL, MaxDistance.INTER_ESTADUAL]:
            print(f"{Colors.RED}Distância máxima inválida!{Colors.RED}")
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

        print(f"\n{Colors.GREEN}Entregador {name} cadastrado com sucesso!{Colors.ENDC}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")

    elif user_type == "enterprise":
        print(f"\n{Colors.BOLD}INFORMAÇÕES DA EMPRESA{Colors.ENDC}")
        name = get_input(f"{Colors.CYAN}Digite o nome da empresa: {Colors.ENDC}").strip()
        cnpj = get_input(f"{Colors.CYAN}Digite o CNPJ (14 dígitos): {Colors.ENDC}", is_cnpj).strip()
        address = get_address_from_input("enterprise")

        enterprise = Enterprise(name, cnpj, address, user_id)
        enterprise.insert()

        # Obter o enterprise_id recém-criado
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM enterprises WHERE cnpj = ? AND user_id = ?", (cnpj, user_id))
            enterprise_id = cursor.fetchone()
            if not enterprise_id:
                print(f"{Colors.RED}Erro: Não foi possível recuperar o ID da empresa!{Colors.RED}")
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

        print(f"\n{Colors.GREEN}Empresa {name} cadastrado com sucesso!{Colors.ENDC}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
