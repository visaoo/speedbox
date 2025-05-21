from classes.resources import *

from validations.validations import get_input, none_word, is_num
from classes.address.address import Address


def get_address_from_input(type_user, client_id=None, enterprise_id=None) -> Address:
    print(f"\n{Colors.BOLD}ENDEREÇO{Colors.ENDC}")
    while True:
        street = get_input(f"{Colors.CYAN}Rua: {Colors.ENDC}", none_word, errorMensage=f"{Colors.RED}Rua não pode ser vazia!.{Colors.ENDC}").strip()

        number = get_input(f"{Colors.CYAN}Número: {Colors.ENDC}",
        lambda x: is_num(x, int), errorMensage=f"{Colors.RED}Número não pode ser vazio e deve ser numérico!{Colors.ENDC}"
        ).strip()
        
        neighborhood = get_input(f"{Colors.CYAN}Bairro: {Colors.ENDC}", none_word, errorMensage=f"{Colors.RED}Bairro não pode ser vazia!.{Colors.ENDC}").strip()
        
        city = get_input(f"{Colors.CYAN}Cidade: {Colors.ENDC}", none_word, errorMensage=f"{Colors.RED}Cidade não pode ser vazia!.{Colors.ENDC}").strip()
        
        state = get_input(f"{Colors.CYAN}Estado: {Colors.ENDC}", none_word, errorMensage=f"{Colors.RED}Estado não pode ser vazia!.{Colors.ENDC}").strip()
        try:
            return Address(street, number, neighborhood, city, state, client_id=client_id, enterprise_id=enterprise_id)
        except ValueError as e:
            print(f"Erro: {e}")
            continue
