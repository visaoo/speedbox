from validations.validations import get_input, none_word

from classes.order import Order, OrderStatus
from app.utils.get_connection import get_connection


def update_order_status_delivery_person(delivery_person_id):
    order_type = get_input("Digite o tipo de pedido (client/enterprise): ", none_word).strip()
    order_id = get_input("Digite o ID do pedido: ", none_word).strip()
    new_status = get_input("Digite o novo status (completed/canceled): ", none_word).strip()
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
