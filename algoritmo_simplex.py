import random

def ler_arquivo(nome_arquivo="funcao.txt"):
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        return [linha.strip() for linha in arquivo.readlines()]

def identificar_tipo_funcao(linha):
    return linha.lower().startswith("max")

def extrair_coeficientes(linha):
    linha = linha[7:].strip()  # Remove "max z =" ou similar
    coef = ""
    coeficientes = []
    i = 0
    n = len(linha)
    
    while i < n:
        if linha[i] == 'x':
            if coef == '' or coef == '+':
                coef = '1.0'
            elif coef == '-':
                coef = '-1.0'
            coeficientes.append(float(coef))
            coef = ""

            i += 1
            while i < n and linha[i].isdigit():
                i += 1
            continue

        if (linha[i].isdigit() or linha[i] == '.') or \
           (linha[i] in ['+', '-'] and (i + 1 < n and (linha[i+1].isdigit() or linha[i+1] == '.'))):
            coef += linha[i]
            i += 1
        else:
            i += 1
    
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
                if coef == '' or coef == '+':
                    coef = '1'
                elif coef == '-':
                    coef = '-1'
                j = i + 1
                var_index = ""
                while j < len(linha) and linha[j].isdigit():
                    var_index += linha[j]
                    j += 1
                var_index = int(var_index) - 1  
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
    matriz_corrigida = [linha[:] for linha in matriz] 

    for i in range(n):
        linha_vazia = all(matriz_corrigida[i][j] == 0 for j in range(n))
        if linha_vazia:
            for k in range(i + 1, n):
                if any(matriz_corrigida[k][j] != 0 for j in range(n)):
                    matriz_corrigida[i], matriz_corrigida[k] = matriz_corrigida[k], matriz_corrigida[i]
                    print(f"Aviso: linha {i + 1} trocada com linha {k + 1} para evitar cofatores nulos.")
                    break
            else:
                raise ValueError(f"A matriz possui linha {i + 1} nula, portanto não é invertível.")


    cofatores = []
    for i in range(n):
        linha_cof = []
        for j in range(n):
            menor = matriz_menor(matriz_corrigida, i, j)
            cof = ((-1) ** (i + j)) * laPlace(menor)
            linha_cof.append(cof)
        cofatores.append(linha_cof)

    adjunta = list(map(list, zip(*cofatores)))

    inversa = []
    for linha in adjunta:
        inversa.append([elem / det for elem in linha])

    return inversa

def multiplicar_matrizes(matriz_a, matriz_b):
    colunas_a = len(matriz_a[0]) if matriz_a else 0
    linhas_b = len(matriz_b)
    
    if colunas_a != linhas_b:
        raise ValueError("Numero de colunas da primeira matriz deve ser igual ao numero de linhas da segunda matriz")
    
    linhas_a = len(matriz_a)
    colunas_b = len(matriz_b[0]) if matriz_b else 0
    resultado = [[0.0 for _ in range(colunas_b)] for _ in range(linhas_a)]
    
    for i in range(linhas_a):
        for j in range(colunas_b):
            soma = 0.0
            for k in range(colunas_a):
                soma += matriz_a[i][k] * matriz_b[k][j]
            resultado[i][j] = soma
    
    return resultado

def main():
    linhas = ler_arquivo()
    numR = len(linhas) - 1
    tipo_maximizacao = identificar_tipo_funcao(linhas[0])  
    coef_funcao_objetivo = extrair_coeficientes(linhas[0]) 
    matriz_restricoes, vetor_resultados = extrair_restricoes(linhas) 


    print(numR)
    print("Maximizacao:", tipo_maximizacao)
    print("Coeficientes da Funcao Objetivo:", coef_funcao_objetivo)  
    print("Matriz de Coeficientes das Restricos:")
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
    
def simplex():
    linhas = ler_arquivo()
    numR = len(linhas) - 1
    tipo_maximizacao = identificar_tipo_funcao(linhas[0])  
    matriz_C = extrair_coeficientes(linhas[0]) 
    matriz_A, matriz_b = extrair_restricoes(linhas) 
    tam_matriz_A = len(matriz_A[0])
    
    matriz_nao_basica = []
    matriz_basica = []
    conjunto_basico = set()

    while True:
        vetor_basico = random.sample(range(tam_matriz_A), numR)
        print("Tentando vetor basico:", vetor_basico)
        
        while tuple(sorted(vetor_basico)) in conjunto_basico:
            vetor_basico = random.sample(range(tam_matriz_A), numR)
        
        matriz_basica = []
        for i in range(numR):  
            linha = []
            for j in vetor_basico:  
                linha.append(matriz_A[i][j])
            matriz_basica.append(linha)
        
        print("Matriz basica construida:")
        for linha in matriz_basica:
            print(linha)
        
        try:
            resultado = laPlace(matriz_basica)
            print("Determinante:", resultado)
            
            if abs(resultado) != 0:
                break
            else:
                conjunto_basico.add(tuple(sorted(vetor_basico)))
        except Exception as e:
            print("Erro no cálculo do determinante:", e)
            conjunto_basico.add(tuple(sorted(vetor_basico)))
            continue

    vetor_nao_basico = []
    for i in range(tam_matriz_A):
        if i not in vetor_basico:
            vetor_nao_basico.append(i)  

    matriz_nao_basica = []
    for i in range(numR):  
        linha = []
        for j in vetor_nao_basico:  
            linha.append(matriz_A[i][j])
        matriz_nao_basica.append(linha)

    print("\nVetor basico final:", vetor_basico)
    print("Matriz basica final:")
    for linha in matriz_basica:
        print(linha)
    
    print("\nVetor nao-basico final:", vetor_nao_basico)
    print("Matriz nao-basica final:")
    for linha in matriz_nao_basica:
        print(linha)

    

if __name__ == "__main__":
    simplex()
