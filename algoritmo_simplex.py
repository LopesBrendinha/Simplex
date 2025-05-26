import random

def ler_arquivo(nome_arquivo="funcao.txt"):
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        return [linha.strip() for linha in arquivo.readlines()]

def identificar_tipo_funcao(linha):
    return linha.lower().startswith("max")

def extrair_coeficientes(linha):
    linha = linha[7:].strip()  
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

def matriz_transposta(matriz):
    return [list(coluna) for coluna in zip(*matriz)]

    
def fase1():
    linhas = ler_arquivo()
    numR = len(linhas) - 1
    coef_originais = extrair_coeficientes(linhas[0])
    matriz_A, matriz_b = extrair_restricoes(linhas)
    tam_matriz_A = len(matriz_A[0])

    # Passo 1: (custo 0 para originais, 1 para artificiais)
    matriz_C = [0.0] * tam_matriz_A + [1.0] * numR

    # Adicionar colunas das variáveis artificiais à matriz A
    for i in range(numR):
        matriz_A[i] += [1.0 if j == i else 0.0 for j in range(numR)]

    # Base inicial: variáveis artificiais (últimas colunas)
    vetor_basico = list(range(tam_matriz_A, tam_matriz_A + numR))
    vetor_nao_basico = [j for j in range(tam_matriz_A + numR) if j not in vetor_basico]

    iteracao = 1
    while True:
        print(f"\n--- Iteração {iteracao} (Fase 1) ---")
        print("Variáveis básicas:", vetor_basico)
        print("Variáveis não-básicas:", vetor_nao_basico)

        # Passo 1: Calcular x_B = B^{-1} * b
        matriz_basica = []
        for i in range(numR):
            linha = []
            for j in vetor_basico:
                linha.append(matriz_A[i][j])
            matriz_basica.append(linha)
        
        try:
            B_inv = matriz_inversa(matriz_basica)
            x_B = multiplicar_matrizes(B_inv, [[bi] for bi in matriz_b])
        except Exception as e:
            print("Erro na inversão:", e)
            return None

        # Passo 2: Calcular custos relativos
        c_B = [matriz_C[j] for j in vetor_basico]
        lambda_T = multiplicar_matrizes([c_B], B_inv)

        N = [[matriz_A[i][j] for j in vetor_nao_basico] for i in range(numR)]
        c_N = [matriz_C[j] for j in vetor_nao_basico]
        r_N = []
        for j in range(len(vetor_nao_basico)):
            a_Nj = [N[i][j] for i in range(numR)]
            r_j = c_N[j] - multiplicar_matrizes(lambda_T, [[x] for x in a_Nj])[0][0]
            r_N.append(r_j)

        print("Custos relativos (r_N):", r_N)

        # Passo 3: Teste de otimalidade
        if min(r_N) >= -1e-10:  
            print("Solução ótima da Fase 1 encontrada!")
            # Verifica se há variáveis artificiais na base
            if any(b >= tam_matriz_A for b in vetor_basico):
                print("Problema infactível!")
                return None
            else:
                # Remove colunas artificiais e retorna base viável
                return vetor_basico, matriz_A[:numR][:tam_matriz_A], matriz_b, coef_originais

        # Passo 4: Variável que entra (menor custo relativo)
        k = r_N.index(min(r_N))
        entra = vetor_nao_basico[k]
        print(f"Variável que entra: x{entra + 1}")

        # Passo 5: Direção simplex
        a_entra = [matriz_A[i][entra] for i in range(numR)]
        y = multiplicar_matrizes(B_inv, [[yi] for yi in a_entra])

        # Passo 6: Variável que sai (razão mínima)
        theta_min = float('inf')
        sai_idx = None
        for i in range(numR):
            if y[i][0] > 1e-10:  # y_i > 0
                theta = x_B[i][0] / y[i][0]
                if theta < theta_min:
                    theta_min = theta
                    sai_idx = i

        if sai_idx is None:
            print("Problema ilimitado na Fase 1!")
            return None

        sai = vetor_basico[sai_idx]
        print(f"Variável que sai: x{sai + 1}")

        # Atualização da base
        vetor_basico[sai_idx] = entra
        vetor_nao_basico[k] = sai
        iteracao += 1

def fase2():
    linhas = ler_arquivo()
    numR = len(linhas) - 1
    coef_originais = extrair_coeficientes(linhas[0]) 
    matriz_A, matriz_b = extrair_restricoes(linhas) 
    tam_matriz_A = len(matriz_A[0]) 
    

    num_var_originais = len(coef_originais)
    num_folgas = tam_matriz_A - num_var_originais
    matriz_C = coef_originais + [0.0] * num_folgas  

    conjunto_basico = set() 
    iteracao = 1

    # Seleção aleatória da base inicial 
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
            det = laPlace(matriz_basica)
            print("Determinante:", det)
            
            if abs(det) > 1e-10:  
                break
            else:
                conjunto_basico.add(tuple(sorted(vetor_basico)))
        except Exception as e:
            print("Erro no cálculo do determinante:", e)
            conjunto_basico.add(tuple(sorted(vetor_basico)))
            continue

    vetor_nao_basico = [j for j in range(tam_matriz_A) if j not in vetor_basico]

    while True:
        print(f"\n--- Iteração {iteracao} ---")
        print("Variáveis básicas:", vetor_basico)
        print("Variáveis não-básicas:", vetor_nao_basico)

        # Passo 1: (x_B = B^{-1} * b)
        B_inv = matriz_inversa(matriz_basica)
        x_B = multiplicar_matrizes(B_inv, [[bi] for bi in matriz_b])
        x_N = [0.0] * len(vetor_nao_basico)  

    
        # Passo 2
        # 2.1:  λ^T = c_B^T * B^{-1}
        c_B = [matriz_C[j] for j in vetor_basico]
        lambda_T = multiplicar_matrizes([c_B], B_inv)

        # 2.2: r_N = c_N - λ^T * N
        N = [[matriz_A[i][j] for j in vetor_nao_basico] for i in range(numR)]
        c_N = [matriz_C[j] for j in vetor_nao_basico]
        r_N = []
        for j in range(len(vetor_nao_basico)):
            a_Nj = [N[i][j] for i in range(numR)]  
            r_j = c_N[j] - multiplicar_matrizes(lambda_T, [[x] for x in a_Nj])[0][0]
            r_N.append(r_j)

        print("Custos relativos (r_N):", r_N)

        # 2.3: 
        k = r_N.index(min(r_N))
        entra = vetor_nao_basico[k]
        print(f"Variável que entra: x{entra + 1}")

        # Passo 3
        if min(r_N) >= 0:
            print("Solução ótima encontrada!")
            break

        # Passo 4: y = B^{-1} * a_entra
        a_entra = [matriz_A[i][entra] for i in range(numR)]
        y = multiplicar_matrizes(B_inv, [[yi] for yi in a_entra])

        # Passo 5: 
        theta_min = float('inf')
        sai_idx = None
        for i in range(numR):
            if y[i][0] > 0:
                theta = x_B[i][0] / y[i][0]
                if theta < theta_min:
                    theta_min = theta
                    sai_idx = i

        if sai_idx is None:
            print("Problema ilimitado!")
            break

        sai = vetor_basico[sai_idx]
        print(f"Variável que sai: x{sai + 1}")

        # Passo 6 
        vetor_basico[sai_idx] = entra
        vetor_nao_basico[k] = sai
        matriz_basica = [[matriz_A[i][j] for j in vetor_basico] for i in range(numR)]
        iteracao += 1

    print("\n--- Fim da Fase 2 ---")

def main():
    # Chamada completa das duas fases
    resultado_fase1 = fase1()
    if resultado_fase1 is None:
        print("Problema infactível ou erro na Fase 1")
    else:
        base_viavel, A, b, c = resultado_fase1
        print("Base viável encontrada:", base_viavel)
    

if __name__ == "__main__":
    fase2()
