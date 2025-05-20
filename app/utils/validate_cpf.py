import re

# Funções de validação
def validate_cpf(cpf):
    return bool(re.match(r"^\d{11}$", cpf))
