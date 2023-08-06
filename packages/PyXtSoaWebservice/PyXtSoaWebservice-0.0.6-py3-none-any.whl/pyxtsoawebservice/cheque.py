#*******************************************************************#
# Consultas Cheques SERASA                                          #
# __  _______ _                                                     #
# \ \/ /_   _(_) __ _  ___ _ __       © 2019 Alexandre Defendi      #
#  \  /  | | | |/ _` |/ _ \ '__|       Created on Nov 01, 2019      #
#  /  \  | | | | (_| |  __/ |       alexandre_defendi@hotmail.com   #
# /_/\_\ |_| |_|\__, |\___|_|                                       #
#               |___/                                               #
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html) #
#*******************************************************************#

import logging

from . import send

_logger = logging.getLogger(__name__)

def ConsultCheque(eMail, Password, Document, CdBank, NrAgency, NrAccount, NrCheckIn, NrCheckFim, Environment='producao'):
    """
    Esta transacao so verifica pendencias financeiras

    :param string seu e-mail cadastrado no Serasa
    :param string sua senha cadastrada no Serasa
    :param string Número do documento (CPF / CNPJ)
    :param string Código Banco no BACEN 
    :param string Número da Agência
    :param string Número da Conta
    :param string Número Cheque Inicial 
    :param string Número Cheque Final
    :param string Ambiente de uso
    
    :return response dict or False
    """
    
    method = 'Cheque'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': Document,
            'Banco': CdBank,
            'Agencia': NrAgency,
            'ContaCorrente': NrAccount,
            'NumeroChequeInicial': NrCheckIn,
            'NumeroChequeFinal': NrCheckFim,
        },
    }
    res = send(method,**args)
    return res
