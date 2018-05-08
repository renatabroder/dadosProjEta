import getDados as gd

# requisitaDados.py
# Biblioteca com a função de proporcionar uma interface que facilite a requisição de dados pela API do PROJETA


def cenario():
    dic = gd.criaDicionarioCenarios()
    for i in range(1,len(dic)+1):
        print('    [%d]: %s' %((i), dic.get(i)))
    
    cen = int(input("  Cenário: "))
    while(dic.get(cen) == None):
        cen = int(input("  Cenário: "))

    if(cen ==  1 or cen == 3): res = 20
    elif(cen == 2): res = 5

    return dic.get(cen), res

def frequencia():
    dic = gd.criaDicionarioFrequencia()
    for i in range(1,len(dic)+1):
        print('    [%d]: %s' %((i), dic.get(i)))

    freq = int(input("  Frequência: "))
    while(dic.get(freq) == None):
        freq = int(input("  Frequência: "))

    return dic.get(freq)

def variavel():
    var = gd.criaDicionarioVariaveis()
    for i in range(1,len(var)):
        print('    [%d]: %s' %((i), var.get(i)))

    variavel = int(input("  Número da variável: "))
    return var.get(variavel)    

def latitude():
    lat = input("  Latitude: ")
    return lat

def longitude():
    lng = input("  Longitude: ")
    return lng

def interface():
    print("\n  Requisições PROJETA")
    print("  Interface para requisitar dados climáticos históricos do site <<https://projeta.cptec.inpe.br/#/dashboard>>\n    (Intervalo Padrão: jan/1961-dez/2005)\n")
    
    cen, res = cenario()
    print()
    freq = frequencia()
    print()
    var = variavel()
    print()
    #lat = latitude()
    #print()
    #lng = longitude()
    #print()


    lat = "-22.972612"
    lng = "-46.371459"
    intervTempo = "1/1961/12/2005/"

    print("Preparando requisição para " + str(cen) + ', ' + str(res) + 'km, ' + str(freq) + ', ' + str(var) + '...')
    dados = gd.getDados(cen, res, freq, intervTempo, var, lat, lng)

    print("\n\nDataframe requisitado:\n")
    print(dados)
    
    return dados