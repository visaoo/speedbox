from app.utils.get_connection import get_connection
from classes.resources import *


def view_open_orders(client_enterprise):
    with get_connection() as conn:
        cursor = conn.cursor()
        if client_enterprise == 'client':
            cursor.execute("SELECT * FROM orders WHERE status IN ('payment_pending', 'pending')")
        if client_enterprise == 'enterprise':
            cursor.execute("SELECT * FROM orders_enterprise WHERE status IN ('payment_pending', 'pending')")
        orders = cursor.fetchall()
    if not orders:
        print(f"{Colors.YELLOW}Nenhum pedido em aberto.{Colors.YELLOW}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
        return
    for order in orders:
        print(f"{Colors.BOLD}{Colors.HEADER}ID:{Colors.ENDC} {Colors.CYAN}{order[0]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Total:{Colors.ENDC} {Colors.GREEN}{order[1]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Data:{Colors.ENDC} {Colors.YELLOW}{order[2]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Descrição:{Colors.ENDC} {Colors.BLUE}{order[3]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Origem:{Colors.ENDC} {Colors.CYAN}{order[7]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Destino:{Colors.ENDC} {Colors.CYAN}{order[6]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Status:{Colors.ENDC} {Colors.RED}{order[8]}{Colors.ENDC}\n")

    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
    
view_open_orders('client')
