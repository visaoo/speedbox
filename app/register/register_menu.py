from classes.resources import *

def register_menu():
    """
    Exibe o menu de opções para o cadastro de diferentes tipos de usuário
    e solicita que o usuário escolha uma opção.

    Returns:
        str: A opção escolhida pelo usuário (1, 2, 3 ou 4).
    """
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}CADASTRO DE USUÁRIO{Colors.ENDC}")
    print(f"{Colors.YELLOW}1.{Colors.ENDC} Cliente")
    print(f"{Colors.YELLOW}2.{Colors.ENDC} Empresa")
    print(f"{Colors.YELLOW}3.{Colors.ENDC} Entregador")
    print(f"{Colors.YELLOW}4.{Colors.ENDC} Voltar")
    
    return input(f"\n{Colors.GREEN}Escolha o tipo de usuário: {Colors.ENDC}")
