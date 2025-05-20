from classes.resources import *
from validations.validations import get_input, none_word, is_phone, is_cpf, is_date
from app.register.register_base_user import register_base_user

from classes.user.client import Client
from classes.address.address import Address

# Adicionar mensagem de erro 

def register_client():
    """
    Realiza o cadastro completo de um novo cliente.

    Primeiro, chama a função `register_base_user` para coletar as informações
    básicas de usuário (nome de usuário, email, senha). Em seguida, solicita
    informações pessoais adicionais (nome completo, CPF, telefone, data de nascimento)
    e detalhes de endereço. Por fim, instancia e insere os objetos `Address`
    e `Client` no banco de dados.
    """
    clear_screen()
    # mostrar registro cliente personalizado
    print(f"\n{Colors.BOLD}CADASTRO DE CLIENTE{Colors.ENDC}")
    
    user = register_base_user("1")
    
    print(f"\n{Colors.BOLD}INFORMAÇÕES PESSOAIS{Colors.ENDC}")
    name = get_input(f"{Colors.CYAN}Nome completo: {Colors.ENDC}", none_word)
    cpf = get_input(f"{Colors.CYAN}CPF: {Colors.ENDC}", is_cpf)
    phone = get_input(f"{Colors.CYAN}TELEFONE: {Colors.ENDC}", is_phone) # perguntar se is_phone ja valida entrada com args
    birth_date = get_input(f"{Colors.CYAN}Data de nascimento (YYYY-MM-DD): {Colors.ENDC}", is_date)

    print(f"\n{Colors.BOLD}ENDEREÇO{Colors.ENDC}")
    street = get_input(f"{Colors.CYAN}Rua: {Colors.ENDC}", none_word)
    number = get_input(f"{Colors.CYAN}Número: {Colors.ENDC}", none_word)
    neighborhood = get_input(f"{Colors.CYAN}Bairro: {Colors.ENDC}", none_word)
    city = get_input(f"{Colors.CYAN}Cidade: {Colors.ENDC}", none_word)
    state = get_input(f"{Colors.CYAN}Estado: {Colors.ENDC}", none_word)
        
    client_id = "101"
        
    address = Address(
        street=street,
        city=city,
        state=state,
        number=number,
        neighborhood=neighborhood,
        client_id=client_id,
    )
    
    address.insert_address(type_user='client')
    
    client = Client(name=name,
                    cpf=cpf,
                    birth_date=birth_date,
                    phone=phone,
                    address=address,
                    )
    client.insert()
    
    print(f"\n{Colors.GREEN}Cliente {name} cadastrado com sucesso!{Colors.ENDC}")
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
