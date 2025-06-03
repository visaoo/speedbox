import re
from datetime import datetime

import phonenumbers


def get_input(prompt, validation=None, errorMensage='Entrada invalida, por favor tente novamente'):
    """
    Solicita entrada do usuário e valida conforme uma função de validação opcional.

    Parâmetros:
        prompt (str): Mensagem exibida ao usuário.
        validation (callable, opcional): Função que recebe o input e retorna True se for válido.
        errorMensage (str): Mensagem de erro a ser exibida em caso de falha na validação.

    Retorna:
        str: Entrada validada do usuário.
    """
    while True:
        userInput = input(prompt)
        if not validation or validation(userInput):
            return userInput
        print(errorMensage)


def is_num(value, num_type):
    """
    Verifica se um valor pode ser convertido para um tipo numérico.

    Parâmetros:
        value (str): Valor a ser testado.
        num_type (type): Tipo numérico (int, float, etc).

    Retorna:
        bool: True se o valor puder ser convertido, False caso contrário.
    """
    try:
        num = num_type(value)
        return True
    except ValueError:
        return False


def is_date(args):
    """
    Valida se uma string representa uma data válida (em diversos formatos) e com idade entre 0 e 120 anos.

    Parâmetros:
        args (str): Data a ser validada.

    Retorna:
        bool: True se a data for válida, False caso contrário.
    """
    maxAge = 120
    patterns = [
        r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$",
        r"^([1-9]|[12][0-9]|3[01])/([1-9]|1[0-2])/\d{4}$",
        r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$",
        r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{2}$",
        r"^([1-9]|[12][0-9]|3[01])-([1-9]|1[0-2])-\d{4}$",
        r"^([1-9]|[12][0-9]|3[01])-([1-9]|1[0-2])-\d{2}$",
        r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{2}$",
        r"^([1-9]|[12][0-9]|3[01])/([1-9]|1[0-2])/\d{2}$"
    ]

    matched = any(re.match(pattern, args) for pattern in patterns)
    if not matched:
        return False

    try:
        try:
            date = datetime.strptime(args, "%d/%m/%Y") if '/' in args else datetime.strptime(args, "%d-%m-%Y")
        except:
            date = datetime.strptime(args, "%d/%m/%y") if '/' in args else datetime.strptime(args, "%d-%m-%y")

        if date > datetime.now():
            return False
        if date < datetime.now().replace(year=datetime.now().year - maxAge):
            return False
        return True
    except:
        return False


def none_word(args):
    """
    Verifica se a string não está vazia ou composta apenas por espaços.

    Parâmetros:
        args (str): Texto de entrada.

    Retorna:
        bool: True se houver conteúdo, False caso contrário.
    """
    return bool(args.strip())


def is_email(email):
    """
    Verifica se um e-mail é válido conforme padrão geral de e-mails.

    Parâmetros:
        email (str): E-mail a ser validado.

    Retorna:
        bool: True se for válido, False caso contrário.
    """
    def _reEmail(email):
        _pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(_pattern, email) is not None

    return _reEmail(email)


def is_phone(args, zipCode='+55'):
    """
    Valida se um número de telefone é válido conforme formato internacional.

    Parâmetros:
        args (str): Número de telefone (sem DDI).
        zipCode (str): Código do país, por padrão o Brasil (+55).

    Retorna:
        bool: True se o número for válido, False caso contrário.
    """
    try:
        _celphone = phonenumbers.parse(zipCode + args, None)
        if not phonenumbers.is_valid_number(_celphone):
            print('numero invalido')
            return False
        return True
    except phonenumbers.NumberParseException:
        print('erro ao tentar validar o numero \n pode haver numeros faltando, ou caracteres invalidos.')
        return False


def is_cpf(cpf):
    """
    Valida se um CPF é válido de acordo com os dígitos verificadores.

    Parâmetros:
        cpf (str): CPF com ou sem pontuação.

    Retorna:
        bool: True se o CPF for válido, False caso contrário.
    """
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma1 * 10 % 11) % 10

    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma2 * 10 % 11) % 10

    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])


def is_cnh(cnh):
    """
    Valida se uma string contém apenas os 11 dígitos de uma CNH,
    removendo quaisquer caracteres não numéricos.
    Parâmetros:
        cnh (str): String que representa a CNH, pode conter pontuação.

    Retorna:
        bool: True se a string, após a limpeza, contiver exatamente 11 dígitos,
              False caso contrário.
    """
    cnh_clean = re.sub(r'\D', '', cnh)

    return len(cnh_clean) == 11


def is_cnpj(cnpj):
    return bool(re.match(r"^\d{14}$", cnpj))


def is_valid_plate(placa):
    """
    Valida se uma placa de veículo segue os padrões antigo ou Mercosul,
    e não contém letras proibidas (I, Q, O).

    Parâmetros:
        placa (str): Placa do veículo (com ou sem hífens/espacos).

    Retorna:
        bool: True se a placa for válida, False caso contrário.
    """
    placa = placa.upper().replace('-', '').replace(' ', '')

    letras_proibidas = {'I', 'Q', 'O'}
    padrao_antigo = re.compile(r'^[A-Z]{3}\d{4}$')
    padrao_mercosul = re.compile(r'^[A-Z]{3}\d[A-Z]\d{2}$')

    formato_valido = (padrao_antigo.match(placa) is not None or
                      padrao_mercosul.match(placa) is not None)

    if not formato_valido:
        return False

    letras = [c for c in placa if c.isalpha()]
    for letra in letras:
        if letra in letras_proibidas:
            return False

    return True

def is_valid_state(state: str) -> bool:
    """
    Verifica se a sigla do estado é válida.
    param: state: Sigla do estado (ex: "SP", "RJ").
    return: True se a sigla for válida, False caso contrário.
    """
    valid_states = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
    return state.upper() in valid_states


def in_enum(entrada_usuario, enum_classe):
    """
    Verifica se a entrada do usuário corresponde a um valor de um Enum.

    Parâmetros:
        entrada_usuario (str): A entrada fornecida pelo usuário.
        enum_classe (Enum): A classe Enum contra a qual validar.

    Retorna:
        bool: True se a entrada for um valor válido do Enum, False caso contrário.
    """
    try:
        # Tenta converter a entrada para um membro do Enum pelo valor
        # Ou verifica se a entrada (como string) é um dos valores do Enum
        return entrada_usuario in [item.value for item in enum_classe]
    except ValueError:
        return False
    except Exception: # Captura outras possíveis exceções ao acessar enum_classe.value
        return False