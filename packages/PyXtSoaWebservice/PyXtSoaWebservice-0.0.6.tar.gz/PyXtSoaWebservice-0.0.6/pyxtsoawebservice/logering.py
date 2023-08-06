#*******************************************************************#
# __  _______ _                                                     #
# \ \/ /_   _(_) __ _  ___ _ __       © 2019 Alexandre Defendi      #
#  \  /  | | | |/ _` |/ _ \ '__|       Created on Nov 01, 2019      #
#  /  \  | | | | (_| |  __/ |       alexandre_defendi@hotmail.com   #
# /_/\_\ |_| |_|\__, |\___|_|                                       #
#               |___/                                               #
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html) #
#*******************************************************************#

# Imports
import logging
from collections import deque
from lxml import etree

# Zeep
#from zeep.plugins import HistoryPlugin
from zeep import Plugin

_logger = logging.getLogger(__name__)

# Plugin do Zeep para incluir o namespace e gerar o log do envio
class XtLogging(Plugin):

    def __init__(self, maxlen=1):
        self._buffer = deque([], maxlen)

    @property
    def last_sent(self):
        last_tx = self._buffer[-1]
        if last_tx:
            return last_tx['sent']

    @property
    def last_received(self):
        last_tx = self._buffer[-1]
        if last_tx:
            return last_tx['received']

    def ingress(self, envelope, http_headers, operation):
        last_tx = self._buffer[-1]
        last_tx['received'] = {
            'envelope': envelope,
            'http_headers': http_headers,
            'operation': operation,
        }
        _logger.info(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers

    def egress(self, envelope, http_headers, operation, binding_options):
#         try:
#             NFe = envelope[0][0][0][2]
#             if NFe:
#                 NFe.set('xmlns','http://www.portalfiscal.inf.br/nfe')
#         except:
#             pass
        xml = etree.tostring(envelope)
        http_headers['POST'] = '/webservices/producao/cep/cep.asmx HTTP/1.1'
        http_headers['Host'] = 'www.soawebservices.com.br'
        http_headers['length'] = str(len(xml))
        
        
        
        
        self._buffer.append({
            'received': None,
            'sent': {
                'envelope': envelope,
                'http_headers': http_headers,
                'operation': operation,
            },
        })
        _logger.info(etree.tostring(envelope, pretty_print=True))
        return envelope, http_headers

