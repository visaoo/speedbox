from classes.address.address import Address

def get_address_from_input(type_user, client_id=None, enterprise_id=None) -> Address:
    while True:
        street = input("Digite a rua: ").strip()
        if not street:
            print("Rua não pode ser vazia!")
            continue
        number = input("Digite o número: ").strip()
        if not number:
            print("Número não pode ser vazio!")
            continue
        neighborhood = input("Digite o bairro: ").strip()
        if not neighborhood and type_user == "client":
            print("Bairro não pode ser vazio para clientes!")
            continue
        city = input("Digite a cidade: ").strip()
        if not city:
            print("Cidade não pode ser vazia!")
            continue
        state = input("Digite o estado: ").strip()
        if not state:
            print("Estado não pode ser vazio!")
            continue
        try:
            return Address(street, number, neighborhood, city, state, client_id=client_id, enterprise_id=enterprise_id)
        except ValueError as e:
            print(f"Erro: {e}")
            continue
