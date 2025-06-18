from app.utils.get_address_from_input import get_address_from_input
from app.utils.get_connection import get_connection
from classes.Auth.auth import Authenticator, EnumUserType
from classes.Auth.auth_service import AuthService
from classes.colors import Colors
from classes.user.client import Client
from classes.user.delivery_person import DeliveryPerson
from classes.user.enterprise import Enterprise
from classes.Vehicle import Vehicle, VehicleType, MaxDistance
from validations.validations import *


def register_user(user_type) -> None:
    """
    Função para registrar um novo usuário no sistema.
    :param user_type: Tipo de usuário a ser registrado (cliente, entregador ou empresa).
    :return: None
    """
    auth = Authenticator(AuthService())
    print(f"\n{Colors.BOLD}CADASTRO DE {user_type.upper()} {Colors.ENDC}")

    # Registrar usuário
    user_id = register_base_user(auth, user_type)
    if not user_id:
        return

    if user_type == EnumUserType.CLIENT.value:
        register_client(user_id)
    elif user_type == EnumUserType.DELIVERY_PERSON.value:
        register_delivery_person(user_id)
    elif user_type == EnumUserType.ENTERPRISE.value:
        register_enterprise(user_id)


def register_base_user(auth, user_type) -> int | None:
    """
    Função para registrar as informações básicas do usuário.
    :param auth: Instância do autenticador para registrar o usuário.
    :param user_type: Tipo de usuário a ser registrado (cliente, entregador ou empresa).
    :return: ID do usuário registrado ou None em caso de erro.
    """
    username = get_input(f"{Colors.CYAN}Nome de usuário: {Colors.ENDC}", none_word).strip()
    email = get_input(f"{Colors.CYAN}Email: {Colors.ENDC}", is_email).strip()
    password = get_input(f"{Colors.CYAN}Senha: {Colors.ENDC}").strip()

    if auth.is_user_registered(username, email):
        print(f"\n{Colors.RED}Erro: Nome de usuário ou email já existe!{Colors.RED}")
        input(f"{Colors.YELLOW}Pressione Enter para tentar novamente...{Colors.ENDC}")
        return None

    auth.register(username, email, password, user_type)
    user = auth.find_user_by_username(username)
    if not user:
        print(f"{Colors.RED}Erro: Não foi possível recuperar o ID do usuário!{Colors.RED}")
        return None
    return user.id

def register_client(user_id) -> None:
    """
    Função para registrar um novo cliente.
    :param user_id: ID do usuário que está sendo registrado.
    :return: None
    """
    print(f"\n{Colors.BOLD}INFORMAÇÕES PESSOAIS{Colors.ENDC}")
    name = get_input(f"{Colors.CYAN}Nome completo: {Colors.ENDC}").strip()
    cpf = get_input(f"{Colors.CYAN}CPF: {Colors.ENDC}", is_cpf).strip()
    birth_date = get_input(f"{Colors.CYAN}Data de nascimento: {Colors.ENDC}", is_date).strip()
    phone = get_input(f"{Colors.CYAN}Telefone: {Colors.ENDC}", is_phone).strip()
    address = get_address_from_input()

    client = Client(name, cpf, phone, birth_date, address, user_id)
    client.insert()
    print(f"\n{Colors.GREEN}Cliente {name} cadastrado com sucesso!{Colors.ENDC}")
    input(f"{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")


def register_delivery_person(user_id) -> None:
    """
    Função para registrar um novo entregador.
    :param user_id: ID do usuário que está sendo registrado.
    :return: None
    """
    print(f"\n{Colors.BOLD}INFORMAÇÕES PESSOAIS{Colors.ENDC}")
    name = get_input(f"{Colors.CYAN}Nome completo: {Colors.ENDC}").strip()
    cpf = get_input(f"{Colors.CYAN}CPF: {Colors.ENDC}", is_cpf).strip()
    cnh = get_input(f"{Colors.CYAN}CNH: {Colors.ENDC}", is_cnh).strip()
    birth_date = get_input(f"{Colors.CYAN}Data de nascimento: {Colors.ENDC}", is_date).strip()
    phone = get_input(f"{Colors.CYAN}Telefone: {Colors.ENDC}", is_phone).strip()
    address = get_address_from_input()

    delivery_person = DeliveryPerson(name, cpf, birth_date, cnh, True, None, phone, address, user_id)
    delivery_person.insert()

    print(f"\n{Colors.BOLD}INFORMAÇÕES DO VEÍCULO{Colors.ENDC}")
    model = get_input(f"{Colors.CYAN}Modelo do veículo: {Colors.ENDC}").strip()
    mark = get_input(f"{Colors.CYAN}Marca do veículo: {Colors.ENDC}").strip()
    plate = get_input(f"{Colors.CYAN}Placa do veículo: {Colors.ENDC}", is_valid_plate).strip()
    type_vehicle = get_input(f"{Colors.CYAN}Tipo de veículo: {Colors.ENDC}", lambda x: in_enum(x, VehicleType)).strip()
    max_distance = get_input(f"{Colors.CYAN}Distância máxima: {Colors.ENDC}").strip()
    
    vehicle = Vehicle(model, mark, plate, VehicleType(type_vehicle), MaxDistance(max_distance))
    vehicle.insert(delivery_person_id=delivery_person.user_id)
    print(f"\n{Colors.GREEN}Entregador {name} cadastrado com sucesso!{Colors.ENDC}")
    input(f"{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")


def register_enterprise(user_id) -> None:
    """
    Função para registrar uma nova empresa.
    :param user_id: ID do usuário que está sendo registrado.
    :return: None
    """
    print(f"\n{Colors.BOLD}INFORMAÇÕES DA EMPRESA{Colors.ENDC}")
    name = get_input(f"{Colors.CYAN}Nome da empresa: {Colors.ENDC}").strip()
    cnpj = get_input(f"{Colors.CYAN}CNPJ: {Colors.ENDC}", is_cnpj).strip()
    address = get_address_from_input()

    enterprise = Enterprise(name, cnpj, address, user_id)
    enterprise.insert()
    print(f"\n{Colors.GREEN}Empresa {name} cadastrada com sucesso!{Colors.ENDC}")
    input(f"{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
