from app.utils.get_address_from_input import get_address_from_input
from classes.order import Order, OrderStatus
from classes.resources import *
from classes.Vehicle import Vehicle
from validations.validations import get_input, none_word
from app.utils.get_product_from_input import get_product_input
from classes.product import Product

def make_order_client(client_id):
    product = get_product_input()
    print(f"{Colors.CYAN}Endereço de origem:{Colors.CYAN}")

    origem = get_address_from_input()
    print(f"{Colors.CYAN}Endereço de destino:{Colors.CYAN}")

    destino = get_address_from_input()

    # Calcular distância (se API estiver configurada)
    try:
        car = Vehicle.calculate_distance(origem.__str__(), destino.__str__(), 'driving-car')
        truck = Vehicle.calculate_distance(origem.__str__(), destino.__str__(), 'driving-hgv')
    except Exception as e:
        print(f"{Colors.RED}Erro ao calcular distância: {e}{Colors.RED}")
        return
    finally:
        distance = car['distancia_km']
        print(f'{Colors.CYAN}Carro: {car}{Colors.CYAN}')
        print(f'{Colors.CYAN}Caminhão: {truck}{Colors.CYAN}')

    confirm = get_input('Deseja confirmar esse pedido? ', none_word)
    match confirm.lower():
        case 'n':
            return #MD implementa isso ae plz
        case 'não':
            return #MD implementa isso ae plz
        case 'nao':
            return #MD implementa isso ae plz
    
    order = Order(origem, destino, OrderStatus.PENDING, distance)
    # Inserir pedido com client_id
    order.insert("client", client_id=client_id)
    id_order = order.get_id('client')
    product.insert('client', id_order)
    

    print(f"\n{Colors.GREEN}Pedido criado com sucesso!{Colors.GREEN}")
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")

