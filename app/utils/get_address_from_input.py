from validations.validations import get_input, none_word, is_num
from classes.address.address import Address


def get_address_from_input(type_user, client_id=None, enterprise_id=None) -> Address:
    while True:
        street = get_input("Digite a rua: ", none_word).strip()
        if not street:
            print("Rua não pode ser vazia!")
            continue
        number = get_input("Digite o número: ", is_num).strip()
        if not number:
            print("Número não pode ser vazio!")
            continue
        neighborhood = get_input("Digite o bairro: ", none_word).strip()
        if not neighborhood and type_user == "client":
            print("Bairro não pode ser vazio para clientes!")
            continue
        city = get_input("Digite a cidade: ", none_word).strip()
        if not city:
            print("Cidade não pode ser vazia!")
            continue
        state = get_input("Digite o estado: ", none_word).strip()
        if not state:
            print("Estado não pode ser vazio!")
            continue
        try:
            return Address(street, number, neighborhood, city, state, client_id=client_id, enterprise_id=enterprise_id)
        except ValueError as e:
            print(f"Erro: {e}")
            continue
