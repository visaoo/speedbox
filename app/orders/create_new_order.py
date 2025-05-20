from classes.resources import *


def create_new_order():
    """
    Guia o usuário através do processo de criação de um novo pedido de entrega,
    solicitando informações como tipo de entrega, quantidade de itens por tamanho,
    endereços de origem e destino, e exibe um resumo para confirmação.
    """
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}NOVO PEDIDO{Colors.ENDC}")

    # 1. Tipo de entrega
    print(f"\n{Colors.BOLD}TIPO DE ENTREGA{Colors.ENDC}")
    print(f"{Colors.YELLOW}1.{Colors.ENDC} Municipal")
    print(f"{Colors.YELLOW}2.{Colors.ENDC} Estadual")
    print(f"{Colors.YELLOW}3.{Colors.ENDC} Interestadual")
    delivery_type = input(f"{Colors.GREEN}Escolha o tipo de entrega (1/2/3): {Colors.ENDC}")

    delivery_map = {"1": "Municipal", "2": "Estadual", "3": "Interestadual"}
    delivery_type_str = delivery_map.get(delivery_type, "Desconhecido")

    if delivery_type_str == "Desconhecido":
        print(f"{Colors.RED}Tipo de entrega inválido!{Colors.ENDC}")
        input(f"\n{Colors.YELLOW}Pressione Enter para voltar...{Colors.ENDC}")
        return

    # 2. Quantidade de itens
    print(f"\n{Colors.BOLD}QUANTIDADE DE ITENS POR TAMANHO{Colors.ENDC}")
    try:
        small_qty = int(input(f"{Colors.CYAN}Itens Pequenos: {Colors.ENDC}"))
        medium_qty = int(input(f"{Colors.CYAN}Itens Médios: {Colors.ENDC}"))
        large_qty = int(input(f"{Colors.CYAN}Itens Grandes: {Colors.ENDC}"))
    except ValueError:
        print(f"{Colors.RED}Por favor, insira apenas números inteiros!{Colors.ENDC}")
        input(f"\n{Colors.YELLOW}Pressione Enter para voltar...{Colors.ENDC}")
        return

    # 3. Endereço de origem
    print(f"\n{Colors.BOLD}ENDEREÇO DE ORIGEM{Colors.ENDC}")
    origin_street = input(f"{Colors.CYAN}Rua: {Colors.ENDC}")
    origin_number = input(f"{Colors.CYAN}Número: {Colors.ENDC}")
    origin_city = input(f"{Colors.CYAN}Cidade: {Colors.ENDC}")

    # 4. Endereço de destino
    print(f"\n{Colors.BOLD}ENDEREÇO DE DESTINO{Colors.ENDC}")
    dest_street = input(f"{Colors.CYAN}Rua: {Colors.ENDC}")
    dest_number = input(f"{Colors.CYAN}Número: {Colors.ENDC}")
    dest_city = input(f"{Colors.CYAN}Cidade: {Colors.ENDC}")

    # 5. Resumo e confirmação
    print(f"\n{Colors.BOLD}RESUMO DO PEDIDO{Colors.ENDC}")
    print(f"{Colors.GREEN}Tipo de entrega: {delivery_type_str}{Colors.ENDC}")
    print(f"{Colors.GREEN}Itens Pequenos: {small_qty}{Colors.ENDC}")
    print(f"{Colors.GREEN}Itens Médios: {medium_qty}{Colors.ENDC}")
    print(f"{Colors.GREEN}Itens Grandes: {large_qty}{Colors.ENDC}")
    print(f"{Colors.GREEN}Origem: Rua {origin_street}, {origin_number} - {origin_city}{Colors.ENDC}")
    print(f"{Colors.GREEN}Destino: Rua {dest_street}, {dest_number} - {dest_city}{Colors.ENDC}")

    confirm = input(f"\n{Colors.CYAN}Confirmar pedido? (s/n): {Colors.ENDC}")
    if confirm.lower() == 's':
        # Adicionar lógica de cálculo de valor baseado no tipo/tamanho
        price = 10 * small_qty + 20 * medium_qty + 30 * large_qty  # exemplo
        print(f"\n{Colors.GREEN}Pedido confirmado com sucesso! Valor total: R$ {price:.2f}{Colors.ENDC}")
    else:
        print(f"\n{Colors.YELLOW}Pedido cancelado.{Colors.ENDC}")
    
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
