import requests as r
import json as j
import pandas as pd

# getDados.py
# Biblioteca com a função de processar a requisição de dados pela API do PROJETA

# Variaveis do sistema PROJETA:
#   cenario: cenários de mudança climática global
#   resolucao: relacionada com a área coberta
#   frequencia: frequência dos dados (ANUAL, MENSAL, DIARIA, 3 HORAS)
#   intervTempo: 
#   var: variável escolhida dentre a lista de variáveis dos dados disponíveis no PROJETA
#   lat: latitude
#   lng: longitude


def criaListaCenarios():
    cenariosJson = r.get("https://projeta.cptec.inpe.br/api/v1/public/models")
    cenarios = j.loads(cenariosJson.text)
    cenarios = cenarios.get('data')

    return cenarios


def criaDicionarioCenarios():
    cenarios = criaListaCenarios()
    cenarios = set([cen.get('couple') for cen in cenarios])
    
    cenarios = sorted(cenarios)

    dic = {}
    i = 1
    for c in cenarios:
        dic[i] = c
        i += 1
    
    return  dic

# Função getCenario(cenario, resolucao):
#   
# Retorna 'modelo/id' para compor link
def getCenario(cenario, resolucao):
    lista = criaListaCenarios()
    for cen in lista:
        if(cen.get('scenario') == 'Historical'):
            if(cen.get('couple') == str(cenario) and cen.get('resolution') == str(resolucao)):
                model, id = cen.get('model'), cen.get('id')
                break

    return str(model)+'/'+str(id)+'/'


def criaListaFrequencia():
    freqJson = r.get("https://projeta.cptec.inpe.br/api/v1/public/intervals")
    freq = j.loads(freqJson.text)
    freq = freq.get('data')
    
    return freq


def criaDicionarioFrequencia():
    freq = criaListaFrequencia()
    dic = {}
    for i in range(len(freq)):
        dic[i+1] = freq[i].get('name')
    return dic


# Função getFrequencia(frequencia):
#
# Retorna 'frequencia/id' para compor link
def getFrequencia(frequencia):
    freq = criaListaFrequencia()

    for f in freq:
        if(f.get('name') == frequencia):
            fr, id = f.get('nickname'), f.get('id')
            return str(fr)+'/'+str(id)+'/'


# Função getVariaveis():
#
# Retorna lista de variáveis dos dados disponíveis no PROJETA
def getVariaveis():
    varJson = r.get("https://projeta.cptec.inpe.br/api/v1/public/variables")
    var = j.loads(varJson.text)

    return [v.get('nickname') for v in var.get('data')]


# Função criaDicionarioVariaveis():
#
# Retorna dicionario com 
def criaDicionarioVariaveis():
    var = getVariaveis()
    dic = {}
    for i in range(len(var)):
        dic[i+1] = var[i]
    return dic


# Função getLink(cenario, resolucao, frequencia, intervTempo, var, lat, lng):
#
# Retorna link de requisição para a API do PROJETA
def getLink(cenario, resolucao, frequencia, intervTempo, var, lat, lng):
    return "https://projeta.cptec.inpe.br/api/v1/public/" + str(getCenario(cenario, resolucao)) + str(getFrequencia(frequencia)) + str(intervTempo) + str(var) + '/' + str(lat) + '/' + str(lng) + '/'

# Função getDados(cenario, resolucao, frequencia, intervTempo, var, lat, lng):
#
# Retorna série temporal de acordo com os dados escolhidos
def getDados(cenario, resolucao, frequencia, intervTempo, var, lat, lng):
    link = getLink(cenario, resolucao, frequencia, intervTempo, var, lat, lng)
    print("\nRequisitando de:\n" + link + '\n')
    
    dadosJson = r.get(link)
    dados = j.loads(dadosJson.text)

    cabecalho = ['Data', dados[0].get('variable')]

    retorno = []
    for linha in dados:
        tupla = []
        tupla.append(linha.get('date'))
        tupla.append(float(linha.get('value')))
        retorno.append(tupla)
    
    retorno = pd.DataFrame.from_records(retorno, index=cabecalho[0], exclude=None, columns=cabecalho, coerce_float=False, nrows=None)

    return retorno