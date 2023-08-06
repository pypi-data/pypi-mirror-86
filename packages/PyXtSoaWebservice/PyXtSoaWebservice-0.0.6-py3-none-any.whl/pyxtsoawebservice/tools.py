#*******************************************************************#
# Bilbioteca de Ferramentas                                         #
# __  _______ _                                                     #
# \ \/ /_   _(_) __ _  ___ _ __       © 2019 Alexandre Defendi      #
#  \  /  | | | |/ _` |/ _ \ '__|       Created on Nov 01, 2019      #
#  /  \  | | | | (_| |  __/ |       alexandre_defendi@hotmail.com   #
# /_/\_\ |_| |_|\__, |\___|_|                                       #
#               |___/                                               #
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html) #
#*******************************************************************#

# Imports
import re

def clearCNPJCPF(Documento):
    res = re.sub('[^0-9]', '', Documento)

def validateCNPJCPF(Documento):
    if validateCNPJ(Documento):
        return True
    if validateCPF(Documento):
        return True
    return False

def validateCNPJ(CNPJ):
    """
    Rotina para validação do CNPJ de Pessoa Juridica.

    :param string CNPJ: CNPJ para ser validado
    :return bool: True or False
    """

    if not CNPJ.isdigit():
        CNPJ = re.sub('[^0-9]', '', CNPJ)

    # verificando o tamano do  cnpj
    if len(CNPJ) != 14:
        return False

    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os digitos
    CNPJ = list(map(int, CNPJ))
    novo = CNPJ[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    if novo == CNPJ:
        return True

    return False


def validateCPF(CPF):
    """
    Rotina para validação do CPF de Pessoa Física.

    :param string CPF: CPF para ser validado
    :return bool: True or False
    """
    CPF = re.sub('[^0-9]', '', CPF)

    if len(CPF) != 11 or CPF == CPF[0] * len(CPF):
        return False

    # Pega apenas os 9 primeiros dígitos do CPF e gera os 2 dígitos que faltam
    CPF = list(map(int, CPF))
    novo = CPF[:9]

    while len(novo) < 11:
        r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11

        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)

    # Se o número gerado coincidir com o número original, é válido
    if novo == CPF:
        return True
    return False
