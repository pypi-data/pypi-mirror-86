from pyxtserasa.negativacao import ListRestrictionCodes, ListLowCodes, createAdress, createDebtor, createRestriction, IncludeConstraint, RegisterAdressOf
#from lxml import etree

eMail = 'alexandre_defendi@hotmail.com'
Senha = 'SxUmRcBeb'
ambiente = 'homologacao'
cnpj_cpf = '00000007000103' 
# tESTE DE OBTENÇÃO DAS LISTAS... TODOS COM SUCESSO
# xml = ListLowCodes(eMail, Senha, ambiente)
# print('Resposta: '+ str(xml['received_xml']))
# xml = ListRestrictionCodes(eMail, Senha, ambiente)
# print('Resposta: '+ str(xml['received_xml']))

endereco = createAdress('81630-130', 'Rua Conde de São João das Duas Barras', '461', '', 'Hauer')
xml = RegisterAdressOf(eMail, Senha, cnpj_cpf, '81630-130', '461', '', ambiente)
print('Resposta: '+ str(xml['received_xml']))

Devedores = []
result = createDebtor('77952944991', endereco, Devedores) 
print(str(Devedores))

restrition = createRestriction('CD', '000120', '1', '01/10/2020', 1500.35)
print(restrition)

xml = IncludeConstraint(eMail, Senha, Devedores, restrition, ambiente)
print('Resposta: '+ str(xml['received_xml']))
