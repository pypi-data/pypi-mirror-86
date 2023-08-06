#*******************************************************************#
# Consultas Administrativas de Parceiros                            #
# __  _______ _                                                     #
# \ \/ /_   _(_) __ _  ___ _ __       © 2019 Alexandre Defendi      #
#  \  /  | | | |/ _` |/ _ \ '__|       Created on Nov 01, 2019      #
#  /  \  | | | | (_| |  __/ |       alexandre_defendi@hotmail.com   #
# /_/\_\ |_| |_|\__, |\___|_|                                       #
#               |___/                                               #
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html) #
#*******************************************************************#

import logging
import re

from . import send

_logger = logging.getLogger(__name__)

def ConsultStatus(eMail, Password):
    """
    Consulta Status dos Serviços

    :param string eMail cadastrado no Serasa
    :param string Password cadastrado no Serasa
    :return response dict or False
    """
    method = 'StatusServicos'
    args = {
        'ambiente': 'producao',
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
        },
    }
    res = send(method,**args)
    return res

def ConsultBalance(eMail, Password):
    """
    Consulta Saldo de sua Conta

    :param string eMail da sua conta no Serasa
    :param string senha da sua conta no Serasa
    :return response dict or False
    """
    method = "Saldo"
    args = {
        'ambiente': 'producao',
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
        },
    }
    res = send(method,**args)
    return res

def ConsultExtract(eMail, Senha, Month, Year):
    """
    Consulta Extrato de sua Conta

    :param string eMail da sua conta no Serasa
    :param string senha da sua conta no Serasa
    :param string Mês de verificação (2 digitos - 00)
    :param string Ano de verificação (4 digitos - 0000)
    :return response dict or False
    """
    method = "Extrato"
    args = {
        'ambiente': 'producao',
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Senha,
            },
            'Mes': Month,
            'Ano': Year,
        },
    }
    res = send(method,**args)
    return res

def ConsultExtractAnaliticDocument(eMail, Senha, Documento):
    """
    Consulta Historico Analitico de sua Conta
    Clientes com grande volume de transações não utilizar esta transação

    :param string eMail da sua conta no Serasa
    :param string senha da sua conta no Serasa
    :return response dict or False
    """
    method = "ExtratoAnalitico"
    args = {
        'ambiente': 'producao',
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Senha,
            },
            'Documento': Documento,
        },
    }
    res = send(method,**args)
    return res
    
def ConsultHistoryDetailed(eMail, Senha, IdDocumento):
    """
    Consulta o Histórico por documento dos serviços utilizados
    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string ID do documento
    :return response dict or False
    """
    method = "HistoricoDetalhado"
    args = {
        'ambiente': 'producao',
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Senha,
            },
            'UniqueID': IdDocumento,
        },
    }
    res = send(method,**args)
    return res

def ConsultCEP(Ambiente, eMail, Senha, NumeroCEP):
    """
    Consulta CEP
    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string Número do CEP
    :return response dict or False
    """
    method = 'ConsultaCEP'
    consulta = {
        'Credenciais': {
            'Email': eMail,
            'Senha': Senha,
        },
        'CEP': re.sub('[^0-9]', '', NumeroCEP),
    }
    args = {
        'ambiente': Ambiente,
        'consulta': consulta,
    }
    res = send(method,**args)
    return res
