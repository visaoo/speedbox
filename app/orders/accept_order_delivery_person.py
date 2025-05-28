from classes.order import Order, OrderStatus
from classes.resources import *
from validations.validations import get_input, none_word
from .open_orders import view_open_orders

def accept_order_delivery_person(delivery_person_id: int) -> None:
    _ = True
    while _:
        try:
            order_type = get_input(f"{Colors.YELLOW}Ver pedidos de clientes ou empresas? {Colors.YELLOW}",none_word).strip()
            if order_type.lower() in ('empresa', 'enterprise'):
                _ = False
                print(f"\n{Colors.YELLOW}Pedido de empresas:{Colors.ENDC}")
                view_open_orders('enterprise')
            elif order_type.lower() in ('client', 'cliente'):
                _ = False
                print(f"\n{Colors.YELLOW}Pedido de clientes:{Colors.ENDC}")
                view_open_orders('client')
            else:
                raise ValueError('Digite cliente ou empresa') 
        except:
            continue
    order_id = get_input(f"\n{Colors.YELLOW}Digite o ID do pedido:{Colors.ENDC}", none_word).strip()

    try:
        order_id = int(order_id)
        Order.update_delivery_person(order_type, order_id, delivery_person_id)
        Order.update_status(order_id, OrderStatus.PENDING, order_type)  # Mantém 'pending' após aceitação
        print(f"\n{Colors.GREEN}Pedido aceito com sucesso!{Colors.GREEN}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")

    except ValueError:
        print(f"\n{Colors.RED}ID do pedido deve ser um número!{Colors.RED}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}Erro ao aceitar pedido: {e}{Colors.RED}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
