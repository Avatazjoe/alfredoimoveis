## Lista de participantes do Brainstorming ##
- Gregory Pacheco
**Susy Ane Pereira** Eliane

## Data inicio desenvolvimento ##
10/04/2014

## Data término desenvolvimento ##
**Em desenvolvimento**

## Programadores responsáveis ##
Gregory Pacheco
Susy Ane Pereira

## Analistas responsáveis ##
**Gregory Pacheco**

## Analistas de qualidade responsáveis ##
**Susy Ane Pereira**

## Versão atual ##
Beta 1.0

## Lista de versões ##
Não há versões liberadas

## Documento de requisitos inicial ##
Storage padrão

## Cliente financiador (stakeholder) ##
**Alfredo Imóveis**

## Banco de dados usado ##
**Postgre SQL versão 9 ou superior**

## Inf. banco de dados ##
**User e senha nos arquivos de configurações**

## Workflow ##
**Workflow descrito na especificação de requisitos, no storage padrão**

## INFORMAÇÕES DO SERVIDOR ##

### Configurações recomendadas do servidor ###
**Dual core 1.5** 2 GB de RAM

### Tipo do servidor de aplicação ###
**Nginx + GUnicorn**

### Inf. sobre servidor de aplicação ###
**Configurações no arquivo de configuração**

### Passos para a configuração do servidor ###

#### Dependências ####

Django==1.6.3
South==0.8.4
argparse==1.2.1
django-bootstrap-form==3.1
django-debug-toolbar==1.1
django-grappelli==2.5.3
django-input-mask==1.3.7.1
psycopg2==2.5.2
sqlparse==0.1.11
wsgiref==0.1.2

### Critérios de segurança ###

#### BACKUP ####

## INSTALAÇÃO ##

## FUNCIONALIDADES ##
### Títulos ###
'''**Títulos de contratos de locação '''**

'''**Títulos que são gerados a partir de um contrato de locação'''**

'''**Descrição completa'''
Estes títulos envolvem:** Valor do aluguel que é puxado do cadastro do imóvel amarrado ao contrato de locação
**Cemig: Conta de luz que deve ser lançada manualmente todo mês** Copasa: Conta de água que deve ser lançada manualmente todo mês
**Condomínio: Valor puxado do cadastro do imóvel** IPTU: Campo puxado do cadastro do imóvel, no entanto só é mostrado no título caso o IPTU ainda não senha sido pago no ano atual
**Outros Valores: Valor lançado manualmente e informado nas observações do título**

'''OPERAÇÕES''''
#### Liquidação de título ####


'''**Resumo sobre a funcionalidade'''
Abate um valor parcial ou integral no valor de um título em aberto**


'''**Descrição completa'''
Esta rotina calcula os juros e multas de acordo com as taxas informados no cadastro de parâmetros**

'''**REGRAS IMPORTANTES ENVOLVIDAS '''
O Cálculo dos juros utiliza a fórmula de juros compostos: M = C** (1 + i)^t
A múlta aplica-se apenas uma vez ao montante original do título, ou seja, não muda de acordo com a quantidade de meses atrasados

O IPTU só é mostrado na tela do título caso ele ainda não tiver sido pago no ano corrente, ao se liquidar um título marcando o parâmetro de liquidação de IPTU o valor do IPTU é gravado junto ao título no campo valor\_iptu\_pago, no imóvel a data do vencimento do título é alterada para o próximo ano.


### Funcionalidade 01 ###
'''**Nome da funcionalidade'''**

'''**Resumo sobre a funcionalidade'''**

'''**Descrição completa'''**

'''OPERAÇÕES''''
#### OPERAÇÃO 01 ####

'''**Nome da funcionalidade'''**

'''**Resumo sobre a funcionalidade'''**

'''**Descrição completa'''**

'''