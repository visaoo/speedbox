from validations.validations import get_input, none_word

from classes.order import Order, OrderStatus
from classes.Vehicle import Vehicle, VehicleType
from app.utils.get_address_from_input import get_address_from_input
from app.utils.get_connection import get_connection


def make_order_client(client_id):
    description = get_input("Digite a descrição do pedido: ", none_word).strip()
    print("Endereço de origem:")
    origem = get_address_from_input("client")
    print("Endereço de destino:")
    destino = get_address_from_input("client")
    
    order = Order(origem, destino, description, OrderStatus.PENDING)
    
    # Calcular distância (se API estiver configurada)
    try:
        car = Vehicle.calculate_distance(origem.__str__(), destino.__str__(), 'driving-car')
        truck = Vehicle.calculate_distance(origem.__str__(), destino.__str__(), 'driving-hgv')
    except Exception as e:
        print(f"Erro ao calcular distância: {e}")
    finally:
        print(f'Carro: {car}')
        print(f'Caminhão: {truck}')
    
    # Inserir pedido com client_id
    order.insert("client", client_id=client_id)
    print("Pedido criado com sucesso!")
