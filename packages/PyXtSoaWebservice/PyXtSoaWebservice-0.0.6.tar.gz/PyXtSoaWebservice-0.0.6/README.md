# README #

Esse README documenta o aplicativo pyXtSoawebservice com as etapas necessárias para colocar a comunicação com o Serasa Experian, utilizando o distribuidor autorizado SOA Webservices (i-Stream Comércio e Serviços Online Ltda).

### Version ###

* Versão desta documentação: 1.0.0 (Jan/2020)

### How do I get set up? ###

* Como faço para instalar:
  1) Instale os pacotes requeridos
  
     pip3 install -r requirements.txt
   
  2) Instale o pacote:

    python3 setup.py build
    python3 setup.py install  
  

## Funções e Procedimentos ##
  
* Consultas Administrativas de Parceiro - consultas dos seus dados de parceiro.

| Funções Administrativas | Parâmetros | Descrição |
|-------------------------|------------|-----------|
| __ConsultStatus__ | __eMail__ | string seu e-mail cadastrado noSerasa |
| * Consulta Status dos Serviços no webservice Serasa | __Password__ | string sua senha cadastrado no Serasa |
| | __Return__ | Retorna dicionário de resposta padrão*** |
| | | |
| __ConsultBalance__ | __eMail__ | string seu e-mail cadastrado no Serasa |
| * Consulta Saldo de sua Conta junto ao Serasa | __Password__ | string sua senha cadastrado no Serasa |
| | __Return__ | Retorna dicionário de resposta padrão*** |
| | | |
| __ConsultBalance__ | __eMail__ | string seu e-mail cadastrado no Serasa |
| * Consulta Extrato de sua conta junto ao Serasa | __Password__ | string sua senha cadastrado no Serasa |
| | __Month__ | Mês de verificação (2 digitos - 00)|
| | __Year__ | Ano de verificação (4 digitos - 0000)|
| | __Return__ | Retorna dicionário de resposta padrão*** |
| | | |
| __ConsultExtractAnaliticDocument__ | __eMail__ | string seu e-mail cadastrado no Serasa |
| * Consulta Historico Analitico de sua Conta junto ao Serasa | __Password__ | string sua senha cadastrado no Serasa |
| __Atenção__ | __Documento__ | Número do CNPJ ***|
| Clientes com grande volume de transações não utilizar esta transação | __Return__ | Retorna dicionário de resposta padrão*** |
| | | |
| __ConsultHistoryDetailed__ | __eMail__ | string seu e-mail cadastrado no Serasa |
| * Consulta o Histórico por documento dos serviços utilizados | __Password__ | string sua senha cadastrado no Serasa |
| | __IdDocumento__ | ID do documento|
| | __Return__ | Retorna dicionário de resposta padrão*** |
| | | |
| __ConsultCEP__ | __Ambiente__ | string producao/homologacao |
| * Consulta CEP, retornando o endereço | __eMail__ | string seu e-mail cadastrado no Serasa | 
| | __Password__ | string sua senha cadastrado no Serasa |
| | __NumeroCEP__ | Código do CEP (somente número ex. 00000000)|
| | __Return__ | Retorna dicionário de resposta padrão*** |
| | | |


| Funções Administrativas | Parâmetros | Descrição |
|-------------------------|------------|-----------|
| __ConsultCheque__ | __eMail__ | string seu e-mail cadastrado no Serasa |
| * Consulta se os cheques constantes no lote, possui alguma restrição como roubo ou cancelamento.| __Password__ | string sua senha cadastrado no Serasa |
|  | __Document__ | string número do CPF/CNPJ do titular do cheque |
|  | __CdBank__ | string Código Bacen da Instituíção que emitiu o cheque |
|  | __NrAgency__ | string Número da agência da Instituíção que emitiu o cheque |
|  | __NrAccount__ | string Número da conta do titular junto a instituíção que emitiu o cheque |
|  | __NrCheckIn__ | string Número inicial do lote do cheque |
|  | __NrCheckFim__ | string Número final do lote do cheque  |
|  | __Environment__ | string/opcional producao/homologacao  |
| | __Return__ | Retorna dicionário de resposta padrão*** |
| | | |
| __ConsultConcentre__ | __eMail__ | string seu e-mail cadastrado no Serasa |
| * Esta transacao so verifica pendencias financeiras| __Password__ | string sua senha cadastrado no Serasa |
| | __Document__ | string número do CPF/CNPJ do consultado |
| | __Additional__ | list Lista de adicionais pedido |
| |	|  [ADD_NENHUM, ADD_QSOCIOS, ADD_PARTICIPA, ADD_RSCORING, ADD_LCREDIT, ADD_CLRISCO, ADD_LIST] |
| | __Environment__ | string/opcional producao/homologacao  |
| | __Return__ | Retorna dicionário de resposta padrão*** |
| | | |
  

  
| Funções de Consultas Fiscais| Parâmetros | Retorno |
|-----------------------------|------------|---------|
| __ConsultFisicalCDCSimple__ | __eMail__ | string seu e-mail cadastrado no Serasa |
| * Consulta se os cheques constantes no lote, possui alguma restrição como roubo ou cancelamento.| __Password__ | string sua senha cadastrado no Serasa |
|  | __Document__ | string número do CPF/CNPJ do titular do cheque |
|  | __CdBank__ | string Código Bacen da Instituíção que emitiu o cheque |
|  | __NrAgency__ | string Número da agência da Instituíção que emitiu o cheque |
|  | __NrAccount__ | string Número da conta do titular junto a instituíção que emitiu o cheque |
|  | __NrCheckIn__ | string Número inicial do lote do cheque |
|  | __NrCheckFim__ | string Número final do lote do cheque |
|  | __Environment__ | string/opcional producao/homologacao |
| | __Return__ | Retorna dicionário de resposta padrão*** |
| | | |
  