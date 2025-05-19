import time
from getpass import getpass
from datetime import datetime
from classes.resources import *

from classes.Auth.auth import Authenticator
from classes.Auth.auth_service import AuthService
from validations.validations import get_input, is_email, none_word

auth = Authenticator(AuthService('database.db'))

# Função para exibir o menu principal
def main_menu():
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}MENU PRINCIPAL{Colors.ENDC}")
    print(f"{Colors.YELLOW}1.{Colors.ENDC} Login")
    print(f"{Colors.YELLOW}2.{Colors.ENDC} Cadastrar")
    print(f"{Colors.YELLOW}3.{Colors.ENDC} Sair")
    
    return input(f"\n{Colors.GREEN}Escolha uma opção: {Colors.ENDC}")

# Função para exibir o menu de cadastro
def register_menu():
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}CADASTRO DE USUÁRIO{Colors.ENDC}")
    print(f"{Colors.YELLOW}1.{Colors.ENDC} Cliente")
    print(f"{Colors.YELLOW}2.{Colors.ENDC} Empresa")
    print(f"{Colors.YELLOW}3.{Colors.ENDC} Entregador")
    print(f"{Colors.YELLOW}4.{Colors.ENDC} Voltar")
    
    return input(f"\n{Colors.GREEN}Escolha o tipo de usuário: {Colors.ENDC}")

# Função para cadastrar um usuário base
def register_base_user(user_select):
    username = get_input(f"{Colors.CYAN}Nome de usuário: {Colors.ENDC}", none_word)
    email = get_input(f"{Colors.CYAN}Email: {Colors.ENDC}", is_email)
    password = get_input(f"{Colors.CYAN}Senha: {Colors.ENDC}", none_word)
    
    user_types = {
        "1": "client",
        "2": "enterprise",
        "3": "delivery_person",
    }

    auth_response = auth.register(username, email, password, user_types[user_select])
    
    if auth_response:
        print(f"\n{Colors.GREEN}Usuário registrado com sucesso!{Colors.ENDC}")
        return {"username": username, "email": email}
    else:
        print(f"{Colors.RED}Email ou senha inválidos. Tente novamente.{Colors.ENDC}")
        return register_base_user(user_select)  # chama novamente se der errado


# Função para cadastrar um cliente
def register_client():
    clear_screen()
    # mostrar registro cliente personalizado
    print(f"\n{Colors.BOLD}CADASTRO DE CLIENTE{Colors.ENDC}")
    
    user = register_base_user("1")
    
    print(f"\n{Colors.BOLD}INFORMAÇÕES PESSOAIS{Colors.ENDC}")
    name = input(f"{Colors.CYAN}Nome completo: {Colors.ENDC}")
    cpf = input(f"{Colors.CYAN}CPF: {Colors.ENDC}")
    
    print(f"\n{Colors.GREEN}Cliente {name} cadastrado com sucesso!{Colors.ENDC}")
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")

# Função para cadastrar uma empresa
def register_enterprise():
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}CADASTRO DE EMPRESA{Colors.ENDC}")
    
    user = register_base_user("2")
    
    print(f"\n{Colors.BOLD}INFORMAÇÕES DA EMPRESA{Colors.ENDC}")
    name = input(f"{Colors.CYAN}Nome da empresa: {Colors.ENDC}")
    cnpj = input(f"{Colors.CYAN}CNPJ: {Colors.ENDC}")
    
    print(f"\n{Colors.GREEN}Empresa {name} cadastrada com sucesso!{Colors.ENDC}")
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")

# Função para cadastrar um entregador
def register_delivery_person():
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}CADASTRO DE ENTREGADOR{Colors.ENDC}")
    
    user = register_base_user("3")
    
    print(f"\n{Colors.BOLD}INFORMAÇÕES PESSOAIS{Colors.ENDC}")
    name = input(f"{Colors.CYAN}Nome completo: {Colors.ENDC}")
    cpf = input(f"{Colors.CYAN}CPF: {Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}INFORMAÇÕES DO VEÍCULO{Colors.ENDC}")
    print(f"{Colors.YELLOW}1.{Colors.ENDC} Moto")
    print(f"{Colors.YELLOW}2.{Colors.ENDC} Carro")
    print(f"{Colors.YELLOW}3.{Colors.ENDC} Bicicleta")
    
    vehicle_choice = input(f"{Colors.CYAN}Escolha o tipo de veículo (1/2/3): {Colors.ENDC}")
    vehicle_map = {"1": "moto", "2": "carro", "3": "bicicleta"}
    vehicle_type = vehicle_map.get(vehicle_choice, "desconhecido")
    
    if vehicle_type == "desconhecido":
        print(f"\n{Colors.RED}Tipo de veículo inválido. Cadastro cancelado.{Colors.ENDC}")
        input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
        return

    print(f"\n{Colors.GREEN}Entregador {name} cadastrado com sucesso como entregador de {vehicle_type}!{Colors.ENDC}")
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")


# Função para fazer login
def login():
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}LOGIN{Colors.ENDC}")
    
    username = get_input(f"{Colors.CYAN}Nome de usuário: {Colors.ENDC}", none_word)
    password = get_input(f"{Colors.CYAN}Senha: {Colors.ENDC}", none_word)

    user_login = auth.login(username, password)
    if user_login:
        print(f"\n{Colors.GREEN}Login realizado com sucesso!{Colors.ENDC}")
        time.sleep(1)

        # Supondo que o sistema ainda precisa perguntar o tipo do usuário manualmente
        user_type = input(f"\n{Colors.CYAN}Simular tipo de usuário (1-Cliente, 2-Empresa, 3-Entregador): {Colors.ENDC}")

        if user_type == "1":
            client_dashboard(username)
        elif user_type == "2":
            enterprise_dashboard(username)
        elif user_type == "3":
            delivery_person_dashboard(username)
    else:
        print(f"\n{Colors.RED}Falha no login. Verifique suas credenciais.{Colors.ENDC}")
        input(f"{Colors.YELLOW}Pressione Enter para tentar novamente...{Colors.ENDC}")


# Dashboard do cliente
def client_dashboard(username):
    while True:
        clear_screen()
        display_logo()
        print(f"\n{Colors.BOLD}DASHBOARD DO CLIENTE{Colors.ENDC} - Bem-vindo, {username}!")
        print(f"\n{Colors.YELLOW}1.{Colors.ENDC} Fazer novo pedido")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} Ver meus pedidos")
        print(f"{Colors.YELLOW}3.{Colors.ENDC} Sair")
        
        choice = input(f"\n{Colors.GREEN}Escolha uma opção: {Colors.ENDC}")
        
        if choice == "1":
            create_new_order()
        elif choice == "2":
            view_orders("cliente")
        elif choice == "3":
            break

# Dashboard da empresa
def enterprise_dashboard(username):
    while True:
        clear_screen()
        display_logo()
        print(f"\n{Colors.BOLD}DASHBOARD DA EMPRESA{Colors.ENDC} - Bem-vindo, {username}!")
        print(f"\n{Colors.YELLOW}1.{Colors.ENDC} Ver pedidos recebidos")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} Sair")
        
        choice = input(f"\n{Colors.GREEN}Escolha uma opção: {Colors.ENDC}")
        
        if choice == "1":
            view_orders("empresa")
        elif choice == "2":
            break

# Dashboard do entregador
def delivery_person_dashboard(username):
    while True:
        clear_screen()
        display_logo()
        print(f"\n{Colors.BOLD}DASHBOARD DO ENTREGADOR{Colors.ENDC} - Bem-vindo, {username}!")
        print(f"\n{Colors.YELLOW}1.{Colors.ENDC} Ver entregas disponíveis")
        print(f"{Colors.YELLOW}2.{Colors.ENDC} Sair")
        
        choice = input(f"\n{Colors.GREEN}Escolha uma opção: {Colors.ENDC}")
        
        if choice == "1":
            view_orders("entregador")
        elif choice == "2":
            break

# Função para criar um novo pedido
def create_new_order():
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
        # Aqui você pode adicionar lógica de cálculo de valor baseado no tipo/tamanho
        price = 10 * small_qty + 20 * medium_qty + 30 * large_qty  # exemplo
        print(f"\n{Colors.GREEN}Pedido confirmado com sucesso! Valor total: R$ {price:.2f}{Colors.ENDC}")
    else:
        print(f"\n{Colors.YELLOW}Pedido cancelado.{Colors.ENDC}")
    
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")


# Função para visualizar pedidos/entregas
def view_orders(user_type):
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

# Função principal
def main():
    welcome_message()
    
    while True:
        choice = main_menu()
        # Login
        if choice == "1":
            login()
        # Register
        elif choice == "2":
            register_choice = register_menu()
            if register_choice == "1":
                register_client()
            elif register_choice == "2":
                register_enterprise()
            elif register_choice == "3":
                register_delivery_person()
        #Exit
        elif choice == "3":
            clear_screen()
            display_logo()
            print(f"\n{Colors.GREEN}Obrigado por usar o SpeedBox! Até logo!{Colors.ENDC}")
            time.sleep(1.5)
            clear_screen()
            break

if __name__ == "__main__":
    main()
