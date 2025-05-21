from classes.resources import *

from validations.validations import get_input, none_word

from classes.order import Order, OrderStatus
from classes.Vehicle import Vehicle
from app.utils.get_address_from_input import get_address_from_input

def make_order_client(client_id):
    description = get_input("Digite a descrição do pedido: ", none_word).strip()
    print(f"{Colors.CYAN}Endereço de origem:{Colors.CYAN}")
    
    origem = get_address_from_input("client")
    print(f"{Colors.CYAN}Endereço de destino:{Colors.CYAN}")
    
    destino = get_address_from_input("client")
    
    order = Order(origem, destino, description, OrderStatus.PENDING)
    
    # Calcular distância (se API estiver configurada)
    try:
        car = Vehicle.calculate_distance(origem.__str__(), destino.__str__(), 'driving-car')
        truck = Vehicle.calculate_distance(origem.__str__(), destino.__str__(), 'driving-hgv')
    except Exception as e:
        print(f"{Colors.RED}Erro ao calcular distância: {e}{Colors.RED}")
        
    finally:
        print(f'{Colors.CYAN}Carro: {car}{Colors.CYAN}')
        print(f'{Colors.CYAN}Caminhão: {truck}{Colors.CYAN}')
    
    # Inserir pedido com client_id
    order.insert("client", client_id=client_id)
    print(f"\n{Colors.GREEN}Pedido criado com sucesso!{Colors.GREEN}")
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
    
