from pyxtserasa.negativacao import ConsultConstraint
#from lxml import etree

eMail = 'alexandre_defendi@hotmail.com'
Senha = 'SxUmRcBeb'
ambiente = 'homologacao'

xml = ConsultConstraint(eMail, Senha, '03014f7d-2633-4973-8283-4523736204f6', ambiente)
print('Resposta: '+ str(xml['received_xml']))
