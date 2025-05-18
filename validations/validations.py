import phonenumbers
import re
from datetime import datetime

def get_input(prompt, validation=None, errorMensage='Entrada invalida, por favor tente novamente'):
    while True:
        userInput = input(prompt)
        if not validation or validation(userInput):
            return userInput
        print(errorMensage)

def is_num(value, num_type):
    try:
        num = num_type(value)
        return True
    except ValueError:
        return False

def is_date(args):
    maxAge = 120
    patterns = [
        r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$",  # dd/mm/yyyy
        r"^([1-9]|[12][0-9]|3[01])/([1-9]|1[0-2])/\d{4}$",    # d/m/yyyy
        r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4}$",  # dd-mm-yyyy
        r"^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{2}$",   # dd-mm-yy
        r"^([1-9]|[12][0-9]|3[01])-([1-9]|1[0-2])-\d{4}$",    # d-m-yyyy
        r"^([1-9]|[12][0-9]|3[01])-([1-9]|1[0-2])-\d{2}$",    # d-m-yy
        r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{2}$",  # dd/mm/yy
        r"^([1-9]|[12][0-9]|3[01])/([1-9]|1[0-2])/\d{2}$"     # d/m/yy
        
    ]
    
    matched = False
    for pattern in patterns:
        if re.match(pattern, args):
            matched = True
            break
    
    if not matched:
        return False
    
    try:
        # Tentar primeiro com formato de 4 dígitos para o ano
        try:
            date = datetime.strptime(args, "%d/%m/%Y") if '/' in args else datetime.strptime(args, "%d-%m-%Y")
        except:
            # Tentar com formato de 2 dígitos para o ano
            try:
                date = datetime.strptime(args, "%d/%m/%y") if '/' in args else datetime.strptime(args, "%d-%m-%y")
            except:
                return False
        
        if date > datetime.now():
            return False
        
        if date < datetime.now().replace(year=datetime.now().year - maxAge):
            return False
        return True
    except:
        return False
    
    
def none_word(args):
    return bool(args.strip())

def is_email(email):
    def _reEmail(email):
        _pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(_pattern, email) is not None
    if _reEmail(email):
        return True
    else:
        return False

def is_phone(args, zipCode='+55'):
    try:
        _celphone = phonenumbers.parse(zipCode + args, None)
        if not phonenumbers.is_valid_number(_celphone):
            print('numero invalido')
            return False
        return True
    except phonenumbers.NumberParseException as e:
        print('erro ao tentar validar o numero \n pode haver numeros faltando, ou caracteres invalidos.')
        return False
    
    
def is_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma1 * 10 % 11) % 10

    soma2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma2 * 10 % 11) % 10

    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])


def is_valid_plate(placa):
    placa = placa.upper().replace('-', '').replace(' ', '')
    
    # Letras não permitidas (I, Q e O)
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

# print(is_valid_plate("ABC-1234"))  # True
# print(is_valid_plate("ABI-1234"))  # False (contém I)
# print(is_valid_plate("ABO1C34"))  # False (contém O)