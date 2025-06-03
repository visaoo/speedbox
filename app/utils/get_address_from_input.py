from classes.address.address import Address
from classes.resources import *
from validations.validations import get_input, is_num, none_word, is_valid_state

def get_address_from_input(client_id=None, enterprise_id=None) -> Address:
    print(f"\n{Colors.BOLD}ENDEREÇO{Colors.ENDC}")
    while True:
        street = get_input(f"{Colors.CYAN}Rua: {Colors.ENDC}", none_word, errorMensage=f"{Colors.RED}Rua não pode ser vazia!.{Colors.ENDC}").strip()

        number = get_input(f"{Colors.CYAN}Número: {Colors.ENDC}",
        lambda x: is_num(x, int), errorMensage=f"{Colors.RED}Número não pode ser vazio e deve ser numérico!{Colors.ENDC}"
        ).strip()

        neighborhood = get_input(f"{Colors.CYAN}Bairro: {Colors.ENDC}", none_word, errorMensage=f"{Colors.RED}Bairro não pode ser vazia!.{Colors.ENDC}").strip()

        city = get_input(f"{Colors.CYAN}Cidade: {Colors.ENDC}", none_word, errorMensage=f"{Colors.RED}Cidade não pode ser vazia!.{Colors.ENDC}").strip()

        # Adicionar validação para o estado
        state = get_input(f"{Colors.CYAN}Estado (UF): {Colors.ENDC}", is_valid_state, errorMensage=f"{Colors.RED}Estado inválido. Use a sigla (ex: SP).{Colors.ENDC}").strip().upper() # Convertendo para maiúsculas

        try:
            return Address(street, number, neighborhood, city, state, client_id=client_id, enterprise_id=enterprise_id)
        except ValueError as e:
            print(f"Erro ao criar endereço: {e}") # Mensagem de erro mais específica
            continue