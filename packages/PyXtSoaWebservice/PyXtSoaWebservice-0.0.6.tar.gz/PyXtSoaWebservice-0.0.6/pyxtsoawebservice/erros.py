#*******************************************************************#
# Erros de Validações                                               #
# __  _______ _                                                     #
# \ \/ /_   _(_) __ _  ___ _ __       © 2019 Alexandre Defendi      #
#  \  /  | | | |/ _` |/ _ \ '__|       Created on Nov 01, 2019      #
#  /  \  | | | | (_| |  __/ |       alexandre_defendi@hotmail.com   #
# /_/\_\ |_| |_|\__, |\___|_|                                       #
#               |___/                                               #
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html) #
#*******************************************************************#

class NonExistentServiceError(Exception):

    def __init__(self, name):
        self.message = 'O serviço %s solicitado não existe.' % name

    def __str__(self):
        return self.message

class NonExistentAmbientError(Exception):

    def __init__(self, name):
        self.message = 'O ambiente %s solicitado não existe.' % name

    def __str__(self):
        return self.message

class CPFCNPJValidError(Exception):

    def __init__(self, document):
        self.message = 'O CPF/CNPJ %s não é válido.' % document

    def __str__(self):
        return self.message

class CPFValidError(Exception):

    def __init__(self, document):
        self.message = 'O CPF %s não é válido.' % document

    def __str__(self):
        return self.message

class CNPJValidError(Exception):

    def __init__(self, document):
        self.message = 'O CNPJ %s não é válido.' % document

    def __str__(self):
        return self.message

class NonExistentConsultAddError(Exception):

    def __init__(self, consult, name):
        self.message = 'A adição %s solicitada a consulta %s não é válida ou é inexistente.' % (name,consult)

    def __str__(self):
        return self.message

class AddParamError(Exception):

    def __init__(self):
        self.message = 'Informe as adições válidas no parâmetro "Additions".'

    def __str__(self):
        return self.message

class AddParamDuplicatedError(Exception):

    def __init__(self):
        self.message = 'Itens duplicados no parâmetro "Additions".'

    def __str__(self):
        return self.message
