from app.utils.get_connection import get_connection
from classes.resources import *


def view_orders_delivery_person(delivery_person_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE delivery_person_id = ? OR (status = 'pending' AND delivery_person_id IS NULL)", (delivery_person_id,))
        client_orders = cursor.fetchall()
        cursor.execute("SELECT * FROM orders_enterprises WHERE delivery_person_id = ? OR (status = 'pending' AND delivery_person_id IS NULL)", (delivery_person_id,))
        enterprise_orders = cursor.fetchall()

    if not (client_orders or enterprise_orders):
        print(f"{Colors.YELLOW}Nenhum pedido disponível.{Colors.YELLOW}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
        return
    print(f"\n{Colors.BOLD}PEDIDOS DE CLIENTES{Colors.ENDC}")

    for order in client_orders:
        print(f"{Colors.BOLD}{Colors.HEADER}ID:{Colors.ENDC} {Colors.CYAN}{order[0]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Total:{Colors.ENDC} {Colors.GREEN}{order[1]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Data:{Colors.ENDC} {Colors.YELLOW}{order[2]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Descrição:{Colors.ENDC} {Colors.BLUE}{order[3]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Status:{Colors.ENDC} {Colors.RED}{order[8]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Origem:{Colors.ENDC} {Colors.CYAN}{order[7]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Destino:{Colors.ENDC} {Colors.CYAN}{order[6]}{Colors.ENDC}\n")
    print("\nPedidos de Empresas:")
    for order in enterprise_orders:
        print(f"{Colors.BOLD}{Colors.HEADER}ID:{Colors.ENDC} {Colors.CYAN}{order[0]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Total:{Colors.ENDC} {Colors.GREEN}{order[1]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Data:{Colors.ENDC} {Colors.YELLOW}{order[2]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Descrição:{Colors.ENDC} {Colors.BLUE}{order[3]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Status:{Colors.ENDC} {Colors.RED}{order[8]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Origem:{Colors.ENDC} {Colors.CYAN}{order[7]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Destino:{Colors.ENDC} {Colors.CYAN}{order[6]}{Colors.ENDC}\n")
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
