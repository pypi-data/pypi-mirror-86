#*******************************************************************#
# Negativação Financeira SERASA                                     #
# __  _______ _                                                     #
# \ \/ /_   _(_) __ _  ___ _ __       © 2019 Alexandre Defendi      #
#  \  /  | | | |/ _` |/ _ \ '__|       Created on Nov 01, 2019      #
#  /  \  | | | | (_| |  __/ |       alexandre_defendi@hotmail.com   #
# /_/\_\ |_| |_|\__, |\___|_|                                       #
#               |___/                                               #
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html) #
#*******************************************************************#

import logging
# import types

from . import send
# from .tools import validateCNPJCPF

DEVEDOR_PRINCIPAL = 'Principal'
DEVEDOR_COOBRIGADO = 'CoObrigado'
LS_DEVEDOR = [DEVEDOR_PRINCIPAL,DEVEDOR_COOBRIGADO]

COMUNICADO_FAC = 'FAC'
COMUNICADO_BOLETO = 'BoletoBancario'
COMUNICADO_CPUBLICA = 'ContasPublicas'
COMUNICADO_AR = 'AR'
LS_COMUNICADO = [COMUNICADO_FAC,COMUNICADO_BOLETO,COMUNICADO_CPUBLICA,COMUNICADO_AR]

CONDICAO_PENDENTE = 'Pendentes'
CONDICAO_ATIVA = 'Ativas'
CONDICAO_ERRO = 'Erro'
CONDICAO_INDISPONIVEL = 'Indiponivel'
CONDICAO_BAIXADA = 'Baixadas'
LS_CONDICAO = [CONDICAO_PENDENTE,CONDICAO_ATIVA,CONDICAO_ERRO,CONDICAO_INDISPONIVEL,CONDICAO_BAIXADA]

_logger = logging.getLogger(__name__)

def ListLowCodes(eMail, Password, Environment='producao'):
    """
    Esta transacao obtem a lista dos códigos de baixa

    :param string seu e-mail cadastrado no Serasa
    :param string sua senha cadastrada no Serasa
    :param string Ambiente de uso
    
    :return response dict or False
    """
    
    method = 'CodigosBaixa'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
        },
    }
    res = send(method,**args)
    return res

def ListRestrictionCodes(eMail, Password, Environment='producao'):
    """
    Esta transacao obtem os códigos de restrição

    :param string seu e-mail cadastrado no Serasa
    :param string sua senha cadastrada no Serasa
    :param string Ambiente de uso
    
    :return response dict or False
    """
    
    method = 'CodigosRestricoes'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
        },
    }
    res = send(method,**args)
    return res

def createDebtor(CNPJCPF, Endereco, Devedores, Tipo=DEVEDOR_PRINCIPAL):
    """
    Cria/Adiciona o devedor na lista de devedores

    :param string seu e-tp_devedor Tipo do devedor Principal ou CoObrigado
    :param string cnpj_cpf número do CNPJ ou CPF sem pontos
    :param list Lista de Devedores
    
    :return response True or False
    """
    if not isinstance(Devedores, list):
        return False
    if len(Devedores) >= 2:
        return False
    for devedor in Devedores:
        if not isinstance(devedor, dict):
            return False
        if devedor.get('TipoDevedor',None) is None:
            return False
        if devedor['Devedores']['TipoDevedor'] == Tipo:
            return False
    devedor = {
        'Documento': CNPJCPF,
        'TipoDevedor': Tipo,
        'Endereco': {
            'CEP': Endereco['CEP'],
            'Logradouro': Endereco['Logradouro'],
            'Numero': Endereco['Numero'],
            'Complemento': Endereco['Complemento'],
            'Bairro': Endereco['Bairro'],
        }
    }
    Devedores.append(devedor)
    return True

def createCheck(cdBank,cdAgencia,nrConta,nrCheque,cdAlineDev):
    cheque = {
        'CodigoBanco': cdBank,
        'Agencia': cdAgencia,
        'ContaCorrente': nrConta,
        'NumeroCheque': nrCheque,
        'Alinea': cdAlineDev,
    }
    return cheque

def createAdress(CEP, Logradouro, Numero, Complemento, Bairro):
    endereco = {
        'CEP': CEP,
        'Logradouro': Logradouro,
        'Numero': Numero,
        'Complemento': Complemento,
        'Bairro': Bairro,
    }
    return endereco

def createRestriction(cdRestricao,nrContrato,nrDocumento,dtVencimento,Valor,dtFimCtrl=False,cheque=False):
    restricao = {
        'CodigoRestricao': cdRestricao,
        'Contrato': nrContrato,
        'NossoNumero': nrDocumento,
        'DataVencimento': dtVencimento,
        'DataFinalContrato': dtFimCtrl,
        'Valor': Valor,
        'RestricaoCheque': cheque,
    }
    return restricao

#CadastrarEndereco

def RegisterAdressOf(eMail, Password, CNPJCPF, CEP, Numero, Complemento, Environment='producao'):
    """
    Esta transacao inclui o endereço do devedor para restrição na base da SERASA

    :param string seu e-mail cadastrado no Serasa
    :param string sua senha cadastrada no Serasa
    :param string Número do CNPJ ou CPF
    :param dict   Dicionário com o Endereço
    :param string Ambiente de uso
    
    :return response dict or False
    """
    method = 'IncluirEnderecoDevedor'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'Documento': CNPJCPF,
            'Endereco': {
                'CEP': CEP,
                'Numero': Numero,
                'Complemento': Complemento,
            },
        },
    }
    res = send(method,**args)
    return res

def IncludeConstraint(eMail, Password, Devedores, Restricao, Environment='producao'):
    """
    Esta transacao inclui uma restrição no documento apresentado na base da SERASA

    :param string seu e-mail cadastrado no Serasa
    :param string sua senha cadastrada no Serasa
    :param list   Devedores para inclusão da negativação
    :param list   Restricao para inclusão da negativação
    :param string Ambiente de uso
    
    :return response dict or False
    """

    method = 'Incluir'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'InclusaoNegativacao': {
                'Devedores': Devedores,
                'Restricao': {
                    'CodigoRestricao': Restricao['CodigoRestricao'],
                    'Contrato': Restricao['Contrato'],
                    'NossoNumero': Restricao['NossoNumero'],
                    'DataVencimento': Restricao['DataVencimento'],
                    'DataFinalContrato': Restricao.get('DataFinalContrato',False),
                    'Valor': Restricao['Valor'],
                    'RestricaoCheque': Restricao['RestricaoCheque'],
                }
            }
        }
    }
    res = send(method,**args)
    return res

def ListConstraint(eMail, Password, Condicao, Environment='producao'):
    """
    Esta transacao retorna a lista de negativacoes cadastradas na base de dados da SERASA Experian

    :param string seu e-mail cadastrado no Serasa
    :param string sua senha cadastrada no Serasa
    :param string Ambiente de uso
    
    :return response dict or False
    """

    if Condicao in (LS_CONDICAO):
        method = 'Lista'
        args = {
            'ambiente': Environment,
            'consulta': {
                'Credenciais': {
                    'Email': eMail,
                    'Senha': Password,
                },
                'Condicao': Condicao,
            }
        }
        res = send(method,**args)
    else:
        res = False
    return res

def ConsultConstraint(eMail, Password, UniqueID, Environment='producao'):
    """
    Consulta uma restrição no documento na base da SERASA

    :param string seu e-mail cadastrado no Serasa
    :param string sua senha cadastrada no Serasa
    :param string a ID cadastrada no Serasa
    :param string Ambiente de uso
    
    :return response dict or False
    """

    method = 'Consulta'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'UniqueID': UniqueID,
        }
    }
    res = send(method,**args)
    return res

def DeleteConstraint(eMail, Password, UniqueID, cdBaixa, dtBaixa, Environment='producao'):
    """
    Consulta uma restrição no documento na base da SERASA

    :param string seu e-mail cadastrado no Serasa
    :param string sua senha cadastrada no Serasa
    :param string a ID cadastrada no Serasa
    :param string Ambiente de uso
    
    :return response dict or False
    """

    method = 'Excluir'
    args = {
        'ambiente': Environment,
        'consulta': {
            'Credenciais': {
                'Email': eMail,
                'Senha': Password,
            },
            'UniqueID': UniqueID,
            'CodigoBaixa': cdBaixa,
            'DataBaixa': dtBaixa,
        }
    }
    res = send(method,**args)
    return res

