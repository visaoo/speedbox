from classes.resources import *
from validations.validations import get_input, none_word, is_phone, is_cpf, is_date, is_valid_plate
from app.register.register_base_user import register_base_user

from classes.user.delivery_person import DeliveryPerson
from classes.Vehicle import Vehicle, VehicleType

def register_delivery_person():
    """
    Realiza o cadastro completo de um novo entregador.

    Primeiro, chama a função `register_base_user` para coletar as informações
    básicas de usuário (nome de usuário, email, senha). Em seguida, solicita
    informações pessoais adicionais (nome completo, CPF, telefone, data de nascimento, CNH) e detalhes do veículo (modelo, marca, placa, distância máxima e tipo de veículo).
    Por fim, instancia e insere os objetos `Vehicle` e `DeliveryPerson` no banco de dados.
    """
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}CADASTRO DE ENTREGADOR{Colors.ENDC}")
    
    user = register_base_user("3")
    
    print(f"\n{Colors.BOLD}INFORMAÇÕES PESSOAIS{Colors.ENDC}")
    name = get_input(f"{Colors.CYAN}Nome completo: {Colors.ENDC}", none_word)
    cpf = get_input(f"{Colors.CYAN}CPF: {Colors.ENDC}", is_cpf, errorMensage=f"{Colors.RED}CPF inválido. Tente novamente.{Colors.ENDC}")
    phone = get_input(f"{Colors.CYAN}TELEFONE: {Colors.ENDC}", is_phone, errorMensage=f"{Colors.RED}Telefone inválido. Tente novamente.{Colors.ENDC}")
    birth_date = get_input(f"{Colors.CYAN}Data de nascimento (YYYY-MM-DD): {Colors.ENDC}", is_date, errorMensage=f"{Colors.RED}Data de nascimento inválida (formato YYYY-MM-DD). Tente novamente.{Colors.ENDC}")
    cnh = get_input(f"{Colors.CYAN}CNH: {Colors.ENDC}", none_word)
    
    client_id = "101"

    print(f"\n{Colors.BOLD}INFORMAÇÕES DO VEÍCULO{Colors.ENDC}")
    model = get_input(f"{Colors.CYAN}Modelo do veículo: {Colors.ENDC}", none_word)
    mark = get_input(f"{Colors.CYAN}Marca do veículo: {Colors.ENDC}", none_word)
    plate = get_input(f"{Colors.CYAN}Placa do veículo: {Colors.ENDC}", is_valid_plate, errorMensage=f"{Colors.RED}A placa digitada não é válida (formato AAA0000 ou ABC1D23). Tente novamente.{Colors.ENDC}")
    
    while True:
        try:
            maximum_distance_str = input(f"{Colors.CYAN}Distância máxima de entrega (em km): {Colors.ENDC}")
            maximum_distance = float(maximum_distance_str)
            if maximum_distance >= 0:
                break
            else:
                print(f"{Colors.RED}A distância máxima deve ser um valor não negativo.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}Por favor, insira um valor numérico para a distância.{Colors.ENDC}")

    print(f"{Colors.YELLOW}1.{Colors.ENDC} Moto")
    print(f"{Colors.YELLOW}2.{Colors.ENDC} Carro")
    print(f"{Colors.YELLOW}3.{Colors.ENDC} Bicicleta")

    while True:
        vehicle_choice_str = input(f"{Colors.CYAN}Escolha o tipo de veículo (1/2/3): {Colors.ENDC}")
        if vehicle_choice_str in ["1", "2", "3"]:
            break
        else:
            print(f"{Colors.RED}Opção inválida. Por favor, escolha 1, 2 ou 3.{Colors.ENDC}")

    vehicle_map = {"1": "moto", "2": "carro", "3": "bicicleta"}
    type_vehicle = vehicle_map[vehicle_choice_str]

    vehicle = Vehicle(model=model,
                      mark=mark,
                      plate=plate,
                      maximum_distance=maximum_distance,
                      type_vehicle=type_vehicle)
    vehicle.insert()
    
    delivery_person = DeliveryPerson(
        name=name,
        cpf=cpf,
        birth_date=birth_date,
        cnh=cnh,
        available=True,
        vehicle=vehicle,
        user=None, # como?
        phone=phone,
        )
    delivery_person.insert()
    
    print(f"\n{Colors.BOLD}INFORMAÇÕES DO VEÍCULO{Colors.ENDC}")
    print(f"{Colors.YELLOW}1.{Colors.ENDC} Moto")
    print(f"{Colors.YELLOW}2.{Colors.ENDC} Carro")
    print(f"{Colors.YELLOW}3.{Colors.ENDC} Bicicleta")
    
    vehicle_choice = input(f"{Colors.CYAN}Escolha o tipo de veículo (1/2/3): {Colors.ENDC}")
    vehicle_map = {"1": VehicleType.MOTO, "2": VehicleType.CARRO, "3": VehicleType.BICICLETA}
    type_vehicle = vehicle_map[vehicle_choice_str]
    
    vehicle_type = type_vehicle
    
    vehicle_type = vehicle_map.get(vehicle_choice, "desconhecido")
    
    if vehicle_type == "desconhecido":
        print(f"\n{Colors.RED}Tipo de veículo inválido. Cadastro cancelado.{Colors.ENDC}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
        return

    print(f"\n{Colors.GREEN}Entregador {name} cadastrado com sucesso como entregador de {vehicle_type}!{Colors.ENDC}")
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")

