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
from decimal import Decimal
from datetime import date
from datetime import datetime
from unicodedata import normalize

def str_normalize(string):
    """
    Remove special characters and strip spaces
    """
    if string:
        if not isinstance(string, str):
            string = str(string, 'utf-8', 'replace')
        string = string.encode('utf-8')
        return normalize('NFKD', string.decode('utf-8')).encode('ASCII', 'ignore').decode()
    return ''

def str_strip_line_feed(string):
    if string:
        if not isinstance(string, str):
            string = str(string, 'utf-8', 'replace')
        remap = {
            ord('\t'): ' ',
            ord('\n'): ' ',
            ord('\f'): ' ',
            ord('\r'): None,      # Delete
        }
        return string.translate(remap).strip()
    return string

def num_format_percent(value):
    if value:
        return Decimal(value) / 100

def num_format_datetime(value):
    """
    Format datetime
    """
    dt_format = '%Y-%m-%dT%H:%M:%I'
    if isinstance(value, datetime):
        return value.strftime(dt_format)
    return value

def num_format_date(value):
    """
    Format date
    """
    dt_format = '%Y-%m-%d'
    if isinstance(value, date):
        return value.strftime(dt_format)
    return value

def num_format_with_comma(value):
    if isinstance(value, float):
        return ('%.2f' % value).replace('.', ',')
    return value