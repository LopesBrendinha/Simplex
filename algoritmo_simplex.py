
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
    num_folga = 0
    restricoes_processadas = []
    num_variaveis_max = 0

    for linha in linhas[1:]:
        coef = ""
        restricao_temp = {}
        partes = linha.split()
        resultado = float(partes[-1])
        vetor_resultados.append(resultado)

        if ">=" in linha:
            tipo_restricao = ">="
        elif "<=" in linha:
            tipo_restricao = "<="
        else:
            tipo_restricao = "="

        i = 0
        while i < len(linha):
            if linha[i].isdigit() or linha[i] in ['+', '-', '.']:
                coef += linha[i]
            elif linha[i] == 'x':
                # Coeficiente padrão
                if coef == '' or coef == '+':
                    coef = '1'
                elif coef == '-':
                    coef = '-1'
                j = i + 1
                var_index = ""
                while j < len(linha) and linha[j].isdigit():
                    var_index += linha[j]
                    j += 1
                var_index = int(var_index) - 1  # x1 vira índice 0
                restricao_temp[var_index] = float(coef)
                num_variaveis_max = max(num_variaveis_max, var_index + 1)
                coef = ""
                i = j - 1
            i += 1

        restricao = [0.0] * num_variaveis_max
        for idx, valor in restricao_temp.items():
            restricao[idx] = valor

        folga = [0.0] * num_folga
        if tipo_restricao == "<=":
            folga.append(1.0)
            num_folga += 1
        elif tipo_restricao == ">=":
            folga.append(-1.0)
            num_folga += 1

        restricao.extend(folga)
        restricoes_processadas.append(restricao)

    num_total_variaveis = num_variaveis_max + num_folga
    for restricao in restricoes_processadas:
        while len(restricao) < num_total_variaveis:
            restricao.append(0.0)
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

def matriz_ajustada(matriz, n):
    matrizAjustada = []
    for i in range(n):
        linha = []
        for j in range(n):
            linha.append(matriz[i][j])
        matrizAjustada.append(linha)
    return matrizAjustada

def matriz_inversa(matriz):
    det = laPlace(matriz)
    if det == 0:
        raise ValueError("A matriz não é invertível.")

    n = len(matriz)

    cofatores = []
    for i in range(n):
        linha_cof = []
        for j in range(n):
            menor = matriz_menor(matriz, i, j)
            cof = ((-1) ** (i + j)) * laPlace(menor)
            linha_cof.append(cof)
        cofatores.append(linha_cof)


    adjunta = list(map(list, zip(*cofatores)))


    inversa = []
    for linha in adjunta:
        inversa.append([elem / det for elem in linha])

    return inversa

def main():
    linhas = ler_arquivo()
    numR = len(linhas) - 1
    tipo_maximizacao = identificar_tipo_funcao(linhas[0])  
    coef_funcao_objetivo = extrair_coeficientes(linhas[0]) 
    matriz_restricoes, vetor_resultados = extrair_restricoes(linhas) 

    print("Maximizacao:", tipo_maximizacao)
    print("Coeficientes da Funcao Objetivo:", coef_funcao_objetivo)  
    print("Matriz de Coeficientes das Restricowes:")
    for linha in matriz_restricoes:
        print(linha)

    print("Vetor de Resultados:", vetor_resultados)
    
    matriz = matriz_ajustada(matriz_restricoes, numR)
    for linha in matriz:
        print(linha)

    print("Determinante: ", laPlace(matriz))

    matriz = matriz_inversa(matriz)
    for linha in matriz:
        print(linha)


if __name__ == "__main__":
    main()
