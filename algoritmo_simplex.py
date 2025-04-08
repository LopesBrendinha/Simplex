def ler_arquivo(nome_arquivo="funcao.txt"):
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
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
    num_variaveis = 0
    num_folga = 0
    restricoes_processadas = []

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

        num_variaveis = max(num_variaveis, len(restricao)) 


        folga = [0] * num_folga  
        if tipo_restricao == "<=":
            folga.append(1) 
        elif tipo_restricao == ">=":
            folga.append(-1)  
        elif tipo_restricao == "=":
            folga.append(0)  

        num_folga += 1
        restricao.extend(folga) 
        restricoes_processadas.append(restricao)


    num_total_variaveis = num_variaveis + num_folga
    for restricao in restricoes_processadas:
        while len(restricao) < num_total_variaveis:
            restricao.append(0)
        matriz_coef.append(restricao)

    return matriz_coef, vetor_resultados

def laPlace(matriz):
    nlinhas = len(matriz)

    if nlinhas == 1:
        return matriz[0][0]
    if nlinhas == 2:
        return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]
    
    else:
        det = 0
        for j in range(nlinhas):
            menor = matriz_menor(matriz, 0, j)
            cofator = (-1) ** j * matriz[0][j] * laPlace(menor)
            det += cofator

    return det

def matriz_menor(matriz, linha_remover, coluna_remover):
    return [
        [elemento for j, elemento in enumerate(linha) if j != coluna_remover]
        for i, linha in enumerate(matriz) if i != linha_remover
    ]

def main():
    linhas = ler_arquivo()
    
    tipo_maximizacao = identificar_tipo_funcao(linhas[0])  
    coef_funcao_objetivo = extrair_coeficientes(linhas[0]) 
    matriz_restricoes, vetor_resultados = extrair_restricoes(linhas) 

    print("Maximizacao:", tipo_maximizacao)
    print("Coeficientes da Funcao Objetivo:", coef_funcao_objetivo)  
    print("Matriz de Coeficientes das Restricowes:")
    for linha in matriz_restricoes:
        print(linha)
    print("Vetor de Resultados:", vetor_resultados)

if __name__ == "__main__":
    main()
