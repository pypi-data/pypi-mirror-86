from pyxtserasa.consults import ConsultStatus, ConsultCEP
#from lxml import etree

eMail = 'alexandre_defendi@hotmail.com'
Senha = 'SxUmRcBeb'
NumeroCEP = '99.999-999'
Ambiente = 'homologacao'

# xml = ConsultaStatus(eMail, Senha)
# print('Resposta: '+ str(xml['received_xml']))

xml = ConsultCEP(Ambiente, eMail, Senha, NumeroCEP)
print('Resposta: '+ str(xml['received_xml']))