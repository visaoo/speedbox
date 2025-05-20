from classes.resources import *
from validations.validations import get_input, none_word
from app.register.register_base_user import register_base_user

from classes.user.enterprise import Enterprise
from classes.address.address import Address

def register_enterprise():
    """
    Realiza o cadastro completo de uma nova empresa.

    Primeiro, chama a função `register_base_user` para coletar as informações
    básicas de usuário (nome de usuário, email, senha). Em seguida, solicita
    detalhes da empresa (nome e CNPJ) e informações completas de endereço.
    Finalmente, instancia e insere os objetos `Address` e `Enterprise` no banco de dados.
    """
    clear_screen()
    display_logo()
    print(f"\n{Colors.BOLD}CADASTRO DE EMPRESA{Colors.ENDC}")
    
    user = register_base_user("2")
       
    print(f"\n{Colors.BOLD}INFORMAÇÕES DA EMPRESA{Colors.ENDC}")
    name = get_input(f"{Colors.CYAN}Nome da empresa: {Colors.ENDC}", none_word)
    cnpj = get_input(f"{Colors.CYAN}CNPJ: {Colors.ENDC}", none_word)

    print(f"\n{Colors.BOLD}ENDEREÇO DA EMPRESA{Colors.ENDC}")
    street = get_input(f"{Colors.CYAN}Rua: {Colors.ENDC}", none_word)
    number = get_input(f"{Colors.CYAN}Número: {Colors.ENDC}", none_word)
    neighborhood = get_input(f"{Colors.CYAN}Bairro: {Colors.ENDC}", none_word)
    city = get_input(f"{Colors.CYAN}Cidade: {Colors.ENDC}", none_word)
    state = get_input(f"{Colors.CYAN}Estado: {Colors.ENDC}", none_word)

    enterprise_address = Address(
        street=street,
        city=city,
        state=state,
        number=number,
        neighborhood=neighborhood
    )
    enterprise_address.insert_address(type_user='enterprise')

    enterprise = Enterprise(
        name=name,
        cnpj=cnpj,
        address=enterprise_address
    )
    enterprise.insert()

    print(f"\n{Colors.GREEN}Empresa {name} cadastrada com sucesso!{Colors.ENDC}")
    input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")
