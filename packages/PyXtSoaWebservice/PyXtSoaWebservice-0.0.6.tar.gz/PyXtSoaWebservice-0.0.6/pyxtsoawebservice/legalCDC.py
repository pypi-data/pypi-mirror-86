#*******************************************************************#
# Consultas de Dados Cadastrais de Pessoas Jurídicas em Geral       #
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

def ConsultLegalCDCSimple(eMail, Password, Document, Environment='producao'):
    """
    Consulta CDC Pessoa Jurídica Simplificada.
    
    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string CNPJ da Empresa Pesquisada (14 digitos)
    :param string Seleção de Ambiente [producao,homologacao]
    :return response dict or False
    """
    method = 'PessoaJuridicaSimplificada'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': Document,
        },
    }
    res = send(method,**args)
    return res

def ConsultLegalCDCExtend(eMail, Password, Document, Environment='producao'):
    """
    Consulta CDC Pessoa Jurídica Estendida

    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string CNPJ da Empresa Pesquisada (8 digitos)
    :param string Seleção de Ambiente [producao,homologacao]
    :return response dict or False
    """
    method = 'PessoaJuridicaEstendida'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': Document,
        },
    }
    res = send(method,**args)
    return res

def ConsultLegalCDCNFe(eMail, Password, Document, Environment='producao'):
    """
    Confirmacao de Dados Cadastrais Pessoa Jurídica - NFe

    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string CNPJ da Empresa Pesquisada (14 digitos)
    :param string Seleção de Ambiente [producao,homologacao]
    :return response dict or False
    """
    method = 'PessoaJuridicaNFe'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': Document,
        },
    }
    res = send(method,**args)
    return res

def ConsultCDCCadastralSynthesis(eMail, Password, Document, Environment='producao'):
    """
    Sintese Cadastral Pessoa Fisica/Juridica

    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string CPF/CNPJ do Pesquisado (8 digitos/14 digitos)
    :param string Seleção de Ambiente [producao,homologacao]
    :return response dict or False
    """
    method = 'SinteseCadastral'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': Document,
        },
    }
    res = send(method,**args)
    return res

def ConsultLegalCDCSimpleNational(eMail, Password, Document, Environment='producao'):
    """
    Pessoa Juridica Simples Nacional

    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string CNPJ da Empresa Pesquisada (14 digitos)
    :param string Seleção de Ambiente [producao,homologacao]
    :return response dict or False
    """
    method = 'PessoaJuridicaSimplesNacional'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': Document,
        },
    }
    res = send(method,**args)
    return res
