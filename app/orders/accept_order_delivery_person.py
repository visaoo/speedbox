from validations.validations import get_input, none_word

from classes.order import Order, OrderStatus


def accept_order_delivery_person(delivery_person_id):
    order_type = get_input("Digite o tipo de pedido (client/enterprise): ", none_word).strip()
    order_id = get_input("Digite o ID do pedido: ", none_word).strip()
    try:
        order_id = int(order_id)
        Order.update_delivery_person(order_type, order_id, delivery_person_id)
        Order.update_status(order_id, OrderStatus.PENDING, order_type)  # Mantém 'pending' após aceitação
        print("Pedido aceito com sucesso!")
    except ValueError:
        print("ID do pedido deve ser um número!")
    except Exception as e:
        print(f"Erro ao aceitar pedido: {e}")
