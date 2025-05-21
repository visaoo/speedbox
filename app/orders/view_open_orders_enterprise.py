from classes.resources import *

from app.utils.get_connection import get_connection


def view_open_orders_enterprise(enterprise_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders_enterprises WHERE enterprise_id = ? AND status IN ('payment_pending', 'pending')", (enterprise_id,))
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
        f"{Colors.BOLD}{Colors.HEADER}Status:{Colors.ENDC} {Colors.RED}{order[4]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Origem:{Colors.ENDC} {Colors.CYAN}{order[5]}{Colors.ENDC}, "
        f"{Colors.BOLD}{Colors.HEADER}Destino:{Colors.ENDC} {Colors.CYAN}{order[6]}{Colors.ENDC}\n")
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")