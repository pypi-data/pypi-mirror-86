#*******************************************************************#
# __  _______ _                                                     #
# \ \/ /_   _(_) __ _  ___ _ __       © 2019 Alexandre Defendi      #
#  \  /  | | | |/ _` |/ _ \ '__|       Created on Nov 01, 2019      #
#  /  \  | | | | (_| |  __/ |       alexandre_defendi@hotmail.com   #
# /_/\_\ |_| |_|\__, |\___|_|                                       #
#               |___/                                               #
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html) #
#*******************************************************************#

class Fields(object):
    "Class with all fields from Response of Service of Serasa/BR"

    @classmethod
    def add(cls, **kwargs):
        obj = cls()
        for (field, value) in kwargs.items():
            setattr(cls, field, value)
        return obj

    @classmethod
    def get(cls, name, default=None):
        obj = cls()
        if hasattr(obj,name):
            return getattr(cls, name)
        else:
            return default
