from pyxtserasa.negativacao import DeleteConstraint, ListLowCodes
#from lxml import etree

eMail = 'alexandre_defendi@hotmail.com'
Senha = 'SxUmRcBeb'
ambiente = 'homologacao'

# xml = ListLowCodes(eMail, Senha, ambiente)
# print('Resposta: '+ str(xml['received_xml']))

xml = DeleteConstraint(eMail, Senha, '03014f7d-2633-4973-8283-4523736204f6', '1', '09/10/2020', ambiente)
print('Resposta: '+ str(xml['received_xml']))
