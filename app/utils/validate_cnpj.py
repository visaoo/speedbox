import re


def validate_cnpj(cnpj):
    return bool(re.match(r"^\d{14}$", cnpj))
