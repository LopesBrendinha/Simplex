def ler_arquivo(nome_arquivo="funcao.txt"):
    with open(nome_arquivo, "r") as arquivo:
        return [linha.strip() for linha in arquivo.readlines()]

def identificar_tipo_funcao(linha):
    return linha.lower().startswith("max")

def extrair_coeficientes(linha):
    linha = linha[7:].strip() 
    coef = ""
    coeficientes = []

    for i, elemento in enumerate(linha):
        if elemento == 'x':
            if coef == '' or coef == '+':
                coef = '1'
            elif coef == '-':
                coef = '-1'
            coeficientes.append(int(coef))
            coef = ""

        if (elemento.isdigit() and (i + 1 < len(linha) and linha[i + 1] == 'x')) or elemento in ['+', '-']:
            coef += elemento

    if coef:
        coeficientes.append(int(coef))

    return coeficientes

def extrair_restricoes(linhas):
    matriz_coef = []
    vetor_resultados = []
    num_variaveis = None
    num_folga = 0
    c = []  

    for linha in linhas[1:]: 
        coef = ""
        restricao = []
        partes = linha.split()  

  
        resultado = int(partes[-1])
        vetor_resultados.append(resultado)


        if ">=" in linha:
            tipo_restricao = ">="
        elif "<=" in linha:
            tipo_restricao = "<="
        else:
            tipo_restricao = "="

        for i, elemento in enumerate(linha):
            if elemento == 'x':
                if coef == '' or coef == '+':
                    coef = '1'
                elif coef == '-':
                    coef = '-1'
                restricao.append(int(coef))
                coef = ""

            if (elemento.isdigit() and (i + 1 < len(linha) and linha[i + 1] == 'x')) or elemento in ['+', '-']:
                coef += elemento

        if num_variaveis is None:
            num_variaveis = len(restricao)  

        for i in range(num_folga, len(matriz_coef)):  
            restricao.append(0)  

        if tipo_restricao == "<=":
            restricao.append(1)  
            c.append(0)  
        elif tipo_restricao == ">=":
            restricao.append(-1)  
            c.append(0)  
            num_folga += 1
        elif tipo_restricao == "=":
            pass  #

        matriz_coef.append(restricao)

    return matriz_coef, vetor_resultados, c

def main():
    linhas = ler_arquivo()
    
    tipo_maximizacao = identificar_tipo_funcao(linhas[0])  
    coef_funcao_objetivo = extrair_coeficientes(linhas[0])  
    matriz_restricoes, vetor_resultados, variaveis_folga = extrair_restricoes(linhas) 

    coef_funcao_objetivo += variaveis_folga

    print("Maximizacao:", tipo_maximizacao)
    print("Coeficientes da Funcao Objetivo:", coef_funcao_objetivo)
    print("Matriz de Coeficientes das Restricoes:")
    for linha in matriz_restricoes:
        print(linha)
    print("Vetor de Resultados:", vetor_resultados)

if __name__ == "__main__":
    main()
