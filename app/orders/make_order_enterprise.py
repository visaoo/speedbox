from validations.validations import get_input, none_word

from ast import Add
from classes.order import Order, OrderStatus
from classes.Vehicle import Vehicle, VehicleType
from app.utils.get_address_from_input import get_address_from_input
from app.utils.get_connection import get_connection


def make_order_enterprise(enterprise_id):
    description = get_input("Digite a descrição do pedido: ").strip()
    print("Endereço de origem:", none_word)
    origem = get_address_from_input("enterprise")
    print("Endereço de destino:")
    destino = get_address_from_input("enterprise")
    
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
    
    # Inserir pedido com enterprise_id
    order.insert("enterprise", enterprise_id=enterprise_id)
    print("Pedido criado com sucesso!")
