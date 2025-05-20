from classes.resources import *

def view_orders(user_type):
    """
    Exibe os pedidos ou entregas com base no tipo de usuário.

    Args:
        user_type (str): O tipo de usuário logado ("client", "enterprise", ou "delivery_person").
    """
    clear_screen()
    display_logo()
    
    if user_type == "cliente":
        print(f"\n{Colors.BOLD}MEUS PEDIDOS{Colors.ENDC}")
        print("Aqui vai os pedidos do cliente")
       
    elif user_type == "empresa":
        print(f"\n{Colors.BOLD}PEDIDOS RECEBIDOS{Colors.ENDC}")
        print("Aqui vai os pedidos recebidos")
        
    elif user_type == "entregador":
        print(f"\n{Colors.BOLD}ENTREGAS DISPONÍVEIS{Colors.ENDC}")
        print("Aqui vai as entregas disponiveis")
    
    input(f"\n{Colors.YELLOW}Pressione Enter para voltar...{Colors.ENDC}")
