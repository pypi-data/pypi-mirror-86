#*******************************************************************#
# Consultas Pendências Financeiras e cartórios estad. SERASA        #
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
from .erros import NonExistentConsultAddError, AddParamError, AddParamDuplicatedError
from .adicionais import ADD_NENHUM, ADD_QSOCIOS, ADD_PARTICIPA, ADD_RSCORING, ADD_LCREDIT, ADD_CLRISCO, ADD_LIST

_logger = logging.getLogger(__name__)

def ConsultCredNet(eMail, Password, Document, State, Additional=[ADD_NENHUM], Environment='producao'):
    """
    Esta transacao so verifica pendencias financeiras

    :param string seu e-mail cadastrado no Serasa
    :param string sua senha cadastrada no Serasa
    :param string Número do documento (CPF / CNPJ)
    :param string Estado a ser pesquisado
    :param string deseja algum adicional (Nenhum, QuadroDeSocios, Participacoes, RiskScoring, LimiteCredito, ClassificacaoRiscoCredito)
    :param string Ambiente de uso
    
    :return response dict or False
    """
    if isinstance(Additional,list):
        if len(Additional) == 0 or ADD_NENHUM in Additional:
            Additional = [ADD_NENHUM]
        else:
            for addin in Additional:
                if not addin in ADD_LIST:
                    raise NonExistentConsultAddError('Pefin',str(addin))
                dups = [i for i,x in enumerate(Additional) if x==addin] 
                if len(dups) > 1:
                    raise AddParamDuplicatedError()    
    else:
        raise AddParamError()
    
    method = 'CredNet'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': Document,
            'Estado': State,
            'Adicionais': Additional,
        },
    }
    res = send(method,**args)
    return res

def ConsultCredNetEstendida(eMail, Password, Document, State, Additional=[ADD_NENHUM], Environment='producao'):
    """
    Esta transacao so verifica pendencias financeiras

    :param string seu e-mail cadastrado no Serasa
    :param string sua senha cadastrada no Serasa
    :param string Número do documento (CPF / CNPJ)
    :param string Estado a ser pesquisado
    :param string deseja algum adicional (Nenhum, QuadroDeSocios, Participacoes, RiskScoring, LimiteCredito, ClassificacaoRiscoCredito)
    :param string Ambiente de uso
    
    :return response dict or False
    """
    if isinstance(Additional,list):
        if len(Additional) == 0 or ADD_NENHUM in Additional:
            Additional = [ADD_NENHUM]
        else:
            for addin in Additional:
                if not addin in ADD_LIST:
                    raise NonExistentConsultAddError('CredNet',str(addin))
                dups = [i for i,x in enumerate(Additional) if x==addin] 
                if len(dups) > 1:
                    raise AddParamDuplicatedError()    
    else:
        raise AddParamError()
    
    method = 'CredNet'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': Document,
            'Estado': State,
            'Adicionais': Additional,
        },
    }
    res = send(method,**args)
    return res
