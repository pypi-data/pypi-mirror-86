from pyxtserasa.consults import ConsultBalance 
#from lxml import etree

eMail = 'alexandre_defendi@hotmail.com'
Senha = 'SxUmRcBeb'

# xml = ConsultaStatus(eMail, Senha)
# print('Resposta: '+ str(xml['received_xml']))

xml = ConsultBalance(eMail, Senha)

print('Resposta: '+ str(xml['received_xml']))