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

from lxml import etree, objectify
from jinja2 import Environment, FileSystemLoader
from . import filters

_logger = logging.getLogger(__name__)

def sanitize_response(response):
    parser = etree.XMLParser(encoding='utf-8')
    tree = etree.fromstring(response.encode('UTF-8'), parser=parser)
    # Remove namespaces inuteis na resposta
    for elem in tree.getiterator():
        if not hasattr(elem.tag, 'find'):
            continue
        i = elem.tag.find('}')
        if i >= 0:
            elem.tag = elem.tag[i + 1:]
    objectify.deannotate(tree, cleanup_namespaces=True)
    return response, objectify.fromstring(etree.tostring(tree))

def render_xml(path, template_name, remove_empty, **data):
    serasa = recursively_normalize(data)
    env = Environment(loader=FileSystemLoader(path), extensions=['jinja2.ext.with_'])
    env.filters["normalize"] = filters.str_strip_line_feed
    env.filters["normalize_str"] = filters.str_normalize
    env.filters["format_percent"] = filters.num_format_percent
    env.filters["format_datetime"] = filters.num_format_datetime
    env.filters["format_date"] = filters.num_format_date
    env.filters["comma"] = filters.num_format_with_comma

    template = env.get_template(template_name)
    xml = template.render(**serasa).replace('\n', '')
    xml = xml.replace('&', '&amp;')
    _logger.info(xml)
    parser = etree.XMLParser(remove_blank_text=True, remove_comments=True, strip_cdata=False)
    root = etree.fromstring(xml, parser=parser)
    # remove espaços em branco
    for element in root.iter("*"):
        if element.text is not None and not element.text.strip():
            element.text = None
    if remove_empty:
        context = etree.iterwalk(root)
        for dummy, elem in context:
            parent = elem.getparent()
            if recursively_empty(elem):
                parent.remove(elem)
        return root
    return etree.tostring(root, encoding=str)

def recursively_normalize(vals):
    for item in vals:
        if type(vals[item]) is str:
            vals[item] = vals[item].strip()
            vals[item] = filters.str_normalize(vals[item])
        elif type(vals[item]) is dict:
            recursively_normalize(vals[item])
        elif type(vals[item]) is list:
            for a in vals[item]:
                recursively_normalize(a)
    return vals

def recursively_empty(e):
    if e.text:
        return False
    return all((recursively_empty(c) for c in e.iterchildren()))

