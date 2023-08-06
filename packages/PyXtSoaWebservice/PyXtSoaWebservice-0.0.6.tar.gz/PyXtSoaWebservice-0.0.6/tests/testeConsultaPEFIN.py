from pyxtserasa.pefin import ConsultPefin
from pyxtserasa import adicionais 

eMail = 'alexandre_defendi@hotmail.com'
Senha = 'SxUmRcBeb'
Documento = '77952944991'
addin = [adicionais.ADD_LCREDIT,adicionais.ADD_QSOCIOS]

xml = ConsultPefin(eMail, Senha, Documento, Additional=addin,Environment='homologacao')

print('Resposta: '+ str(xml['received_xml']))