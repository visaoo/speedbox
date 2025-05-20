
from classes.order import Order, OrderStatus
from classes.Vehicle import Vehicle, VehicleType
from app.utils.get_address_from_input import get_address_from_input
from app.utils.get_connection import get_connection

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
