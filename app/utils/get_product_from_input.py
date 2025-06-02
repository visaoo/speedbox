from classes.product import Product
from classes.resources import *
from validations.validations import get_input, is_num, none_word


def get_product_input() -> Product:
    print(f"\n{Colors.BOLD}Produto{Colors.ENDC}")
    while True:
        name = get_input(f"{Colors.CYAN}Nome: {Colors.ENDC}", none_word, errorMensage=f"{Colors.RED}Nome não pode ser vazio!.{Colors.ENDC}").strip()

        description = get_input(f"{Colors.CYAN}Descrição: {Colors.ENDC}", none_word, errorMensage=f"{Colors.RED}Bairro não pode ser vazia!.{Colors.ENDC}").strip()

        weight = get_input(f"{Colors.CYAN}Peso(em Kg): {Colors.ENDC}",
        lambda x: is_num(x, float), errorMensage=f"{Colors.RED}Peso não pode ser vazio e deve ser numérico!{Colors.ENDC}"
        ).strip()
        
        size = get_input(f"{Colors.CYAN}Tamanho(em cm): {Colors.ENDC}",
        lambda x: is_num(x, float), errorMensage=f"{Colors.RED}Tamanho não pode ser vazio e deve ser numérico!{Colors.ENDC}"
        ).strip()


        try:
            return Product(name=name, description=description, weight=weight, size=size)
        except ValueError as e:
            print(f"Erro: {e}")
            continue