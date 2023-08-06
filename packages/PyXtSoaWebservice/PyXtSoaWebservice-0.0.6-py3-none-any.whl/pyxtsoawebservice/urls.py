#*******************************************************************#
# __  _______ _                                                     #
# \ \/ /_   _(_) __ _  ___ _ __       © 2019 Alexandre Defendi      #
#  \  /  | | | |/ _` |/ _ \ '__|       Created on Nov 01, 2019      #
#  /  \  | | | | (_| |  __/ |       alexandre_defendi@hotmail.com   #
# /_/\_\ |_| |_|\__, |\___|_|                                       #
#               |___/                                               #
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html) #
#*******************************************************************#

# Local Imports
from .erros import NonExistentAmbientError, NonExistentServiceError

# Ambiente
PRODUCAO = 'producao'
HOMOLOGACAO = 'homologacao'

# Serviços
ADMINISTRACAO = 'administracao'
CEP = 'ConsultaCEP'
CDC = 'cdc'
PEFIN = 'Pefin' 
CREDNET = 'crednet'
CONCENTRE = 'concentre'
RECHEQUE = 'recheque'
NEGATIVACAO = 'negativacao'
ADMINISTRATIVOS = ['StatusServicos','Saldo','Extrato','ExtratoAnalitico','ExtratoAnaliticoPorDocumento','HistoricoDetalhado']
NEGATIVACOES = ['CodigosBaixa','CodigosRestricoes','Consulta','Excluir','Incluir','IncluirEnderecoDevedor','Lista']


URLS = {
    PRODUCAO: {
        ADMINISTRACAO: 'https://www.soawebservices.com.br/webservices/producao/sws/administracao.asmx?WSDL',
        CEP: 'https://www.soawebservices.com.br/webservices/producao/cep/cep.asmx?WSDL',
        CDC: 'https://www.soawebservices.com.br/webservices/producao/cdc/cdc.asmx?WSDL',
        PEFIN: 'https://www.soawebservices.com.br/webservices/producao/serasa/pefin.asmx?WSDL', 
        CREDNET: 'https://www.soawebservices.com.br/webservices/producao/serasa/crednet.asmx?WSDL',
        CONCENTRE: 'https://www.soawebservices.com.br/webservices/producao/serasa/concentre.asmx?WSDL',
        RECHEQUE: 'https://www.soawebservices.com.br/webservices/producao/serasa/cheques.asmx?WSDL',
        NEGATIVACAO: 'https://www.soawebservices.com.br/webservices/producao/serasa/negativacao.asmx?WSDL',
    },
    HOMOLOGACAO: {
        CEP: 'http://www.soawebservices.com.br/webservices/test-drive/cep/cep.asmx?WSDL',
        CDC: 'https://www.soawebservices.com.br/webservices/test-drive/cdc/cdc.asmx?WSDL',
        PEFIN: 'https://www.soawebservices.com.br/webservices/test-drive/serasa/pefin.asmx?WSDL', 
        CREDNET: 'https://www.soawebservices.com.br/webservices/test-drive/serasa/crednet.asmx?WSDL',
        CONCENTRE: 'https://www.soawebservices.com.br/webservices/test-drive/serasa/concentre.asmx?WSDL',
        RECHEQUE: 'https://www.soawebservices.com.br/webservices/test-drive/serasa/cheques.asmx?WSDL',
        NEGATIVACAO: 'https://www.soawebservices.com.br/webservices/test-drive/serasa/negativacao.asmx?WSDL',
    },
}

def url_servico(ambiente, servico):
    if servico in (ADMINISTRATIVOS):
        ambiente = PRODUCAO
        servico = ADMINISTRACAO
    if servico in (NEGATIVACOES):
        servico = NEGATIVACAO
    if not bool(URLS.get(ambiente)):
        raise NonExistentAmbientError(ambiente)
    elif not bool(URLS[ambiente].get(servico)):
        raise NonExistentServiceError(servico)
    return URLS[ambiente][servico]

