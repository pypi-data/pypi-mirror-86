from pyxtserasa.consults import ConsultExtract, ConsultStatus
#from lxml import etree

eMail = 'alexandre_defendi@hotmail.com'
Senha = 'SxUmRcBeb'
Mes = '09'
Ano = '2019'

# xml = ConsultaStatus(eMail, Senha)
# print('Resposta: '+ str(xml['received_xml']))

ConsultStatus(eMail, Senha)
xml = ConsultExtract(eMail, Senha, Mes, Ano)

print('Resposta: '+ str(xml['received_xml']))