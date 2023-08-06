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
import os
import requests
import operator
import urllib3

from lxml import etree

# Local Imports
from .logering import XtLogging
from .urls import url_servico
from .xml import render_xml, sanitize_response
#from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Zeep
from requests import Session
from zeep import Client
from zeep.transports import Transport
from zeep.plugins import HistoryPlugin
from zeep import Plugin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#logging.basicConfig(level=logging.DEBUG)
_logger = logging.getLogger(__name__)

def _get_client(base_url, transport):
    history = XtLogging()
    client = Client(base_url, transport=transport, plugins=[history])
    return client

def _list_services(client):
    res = {}
    for service in client.wsdl.services.values():
        _logger.debug(service.name)
        ports = []
        for port in service.ports.values():
            operations = sorted(
                port.binding._operations.values(),
                key=operator.attrgetter('name'))
            
            for operation in operations:
                PortDescription = [operation.name,operation.input.signature()]
                _logger.debug("method: %s, input: %s" % (PortDescription[0], PortDescription[1]))
                ports.append(PortDescription)
        res[service.name] = ports
        return res

def send(method, **kwargs):
    consulta = kwargs["consulta"]
    base_url = url_servico(kwargs["ambiente"],method)
    _logger.debug(base_url)
    session = _get_session()
    transport = Transport(session=session)
    try:
        client = _get_client(base_url, transport)
    except Exception as e:
        return {
            'sent_xml': False,
            'received_xml': str(e),
            'object': None,
        }
    return _send_zeep(client, method, consulta)
    
def _send_zeep(client, method, request_data):
    #requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    with client.settings(raw_response=True):
        response_request = client.service[method](**request_data)
        response, obj = sanitize_response(response_request.text)
        return {
            'sent_xml': response_request.request.body,
            'received_xml': response,
            'object': obj.Body.getchildren()[0]
        }

def _get_session():
    session = Session()
    session.verify = False
    return session

