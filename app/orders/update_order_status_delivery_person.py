from classes.resources import *

from validations.validations import get_input, none_word

from classes.order import Order, OrderStatus
from app.utils.get_connection import get_connection


def update_order_status_delivery_person(delivery_person_id):
    order_type = get_input("Digite o tipo de pedido (client/enterprise): ", none_word).strip()
    order_id = get_input(f"\n{Colors.YELLOW}Digite o ID do pedido:{Colors.ENDC}", none_word).strip()

    new_status = get_input(f"{Colors.CYAN}Digite o novo status (completed/canceled): {Colors.ENDC}", none_word).strip()
    
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
                print(f"\n{Colors.GREEN}Status atualizado com sucesso!{Colors.GREEN}")
                input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
                
            else:
                print(f"\n{Colors.RED}Erro: Você não é o entregador responsável por este pedido ou o pedido não existe.{Colors.RED}")
                input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
    except KeyError:
        print(f"\n{Colors.RED}Status inválido! Use 'completed' ou 'canceled'.{Colors.RED}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
    except ValueError:
        print(f"\n{Colors.RED}ID do pedido inválido!{Colors.RED}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}Erro ao atualizar status: {e}{Colors.RED}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
