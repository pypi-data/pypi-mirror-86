#*******************************************************************#
# Consultas de Dados Cadastrais de Pessoas Físicas em Geral         #
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

def ConsultFisicalCDCSimple(eMail, Password, Document, Birthday, Environment='producao'):
    """
    Consulta CDC Pessoa Fisica Simplificada.
    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string CPF da Pessoa Pesquisada (8 digitos)
    :param string Data de Nascimento do Pesquisado (DD-MM-YYYY)
    :param string Seleção de Ambiente [producao,homologacao]
    :return response dict or False
    """
    method = 'PessoaFisicaSimplificada'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': Document,
            'DataNascimento': Birthday,
        },
    }
    res = send(method,**args)
    return res

def ConsultFisicalCDCExtend(eMail, Password, Document, Environment='producao'):
    """
    Consulta CDC Pessoa Fisica Estendida

    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string CPF da Pessoa Pesquisada (8 digitos)
    :param string Seleção de Ambiente [producao,homologacao]
    :return response dict or False
    """
    method = 'PessoaFisicaEstendida'
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

def ConsultFisicalCDCNFe(eMail, Password, Document, Birthday, Environment='producao'):
    """
    Confirmacao de Dados Cadastrais Pessoa Fisica - NFe

    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string CPF da Pessoa Pesquisada (8 digitos)
    :param string Data de Nascimento do Pesquisado (DD-MM-YYYY)
    :param string Seleção de Ambiente [producao,homologacao]
    :return response dict or False
    """
    method = 'PessoaFisicaNFe'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': Document,
            'DataNascimento': Birthday,
        },
    }
    res = send(method,**args)
    return res

def ConsultFisicalCDCNFeNoBirthday(eMail, Password, Document, Environment='producao'):
    """
    Confirmacao de Dados Cadastrais Pessoa Fisica - NFe
    Consulta sem Data de Nascimento

    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string CPF da Pessoa Pesquisada (8 digitos)
    :param string Seleção de Ambiente [producao,homologacao]
    :return response dict or False
    """
    method = 'PessoaFisicaNFeSemDataNascimento'
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

def ConsultFisicalCDCLocator(eMail, Password, Name, CEP, State, City, Type, Environment='producao'):
    """
    Consulta CDC Pessoa Fisica Localizador

    :param string eMail cadastrado no Serasa
    :param string senha cadastrado no Serasa
    :param string Nome da Pessoa Pesquisada
    :param string CEP do endereço do Pesquisado (NNNNNNNN)
    :param string Seleção de Ambiente [producao,homologacao]
    :return response dict or False
    """
    method = 'PessoaFisicaLocalizador'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Nome': Name,
            'CEP': CEP,
            'Estado': State,
            'Cidade': City,
            'Exata': Type,
        },
    }
    res = send(method,**args)
    return res
