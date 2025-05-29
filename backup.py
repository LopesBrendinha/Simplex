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
        linha = linha.strip()  # Remove espaços em branco no início e no final
        if not linha:  # Verifica se a linha está vazia
            continue  # Ignora linhas vazias

        coef = ""
        restricao_temp = {}
        partes = linha.split()
        
        if len(partes) < 1:  # Verifica se partes tem elementos
            continue  # Ignora linhas que não têm elementos

        resultado = float(partes[-1])  # Último elemento é o resultado
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
    # Passo 0: Leitura dos dados
    linhas = ler_arquivo()
    numR = len(linhas) - 1
    coef_originais = extrair_coeficientes(linhas[0])
    matriz_A, matriz_b = extrair_restricoes(linhas)

    # Cálculo de variáveis
    num_var_originais = len(coef_originais)
    tam_matriz_A = len(matriz_A[0]) if matriz_A else 0  # Variáveis originais + folgas
    num_folgas = tam_matriz_A - num_var_originais

    # --------------------------------------------------------------------------
    # CORREÇÃO CRÍTICA: Vetor de custos completo (originais + folgas + artificiais)
    matriz_C = [0.0] * num_var_originais + [0.0] * num_folgas + [1.0] * numR
    # --------------------------------------------------------------------------

    # Adicionar colunas artificiais à matriz A
    for i in range(numR):
        if i < len(matriz_A):  # Verifica se a linha existe
            matriz_A[i] += [1.0 if j == i else 0.0 for j in range(numR)]
        else:
            print(f"Aviso: não há linha {i} em matriz_A. Verifique a construção da matriz.")

    # Base inicial: variáveis artificiais (últimas colunas)
    vetor_basico = list(range(tam_matriz_A, tam_matriz_A + numR))
    vetor_nao_basico = [j for j in range(tam_matriz_A + numR) if j not in vetor_basico]

    iteracao = 1
    while True:
        print(f"\n--- Iteração {iteracao} (Fase 1) ---")
        print(f"Variáveis básicas: {vetor_basico}")
        print(f"Variáveis não-básicas: {vetor_nao_basico}")

        # Passo 1: Calcular solução básica (x_B = B^{-1} * b)
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
            print(f"Erro na inversão: {e}")
            return None

        # Passo 2: Calcular custos relativos
        c_B = [matriz_C[j] for j in vetor_basico]
        lambda_T = multiplicar_matrizes([c_B], B_inv)

        N = [[matriz_A[i][j] for j in vetor_nao_basico] for i in range(numR)]
        r_N = []
        for j in range(len(vetor_nao_basico)):
            a_Nj = [N[i][j] for i in range(numR)]
            r_j = matriz_C[vetor_nao_basico[j]] - multiplicar_matrizes(lambda_T, [[x] for x in a_Nj])[0][0]
            r_N.append(r_j)

        print("Custos relativos (r_N):", [round(r, 4) for r in r_N])

        # Passo 3: Teste de otimalidade
        if all(r >= -1e-10 for r in r_N):
            print("\nFase 1 concluída com sucesso!")

            # Verifica se há variáveis artificiais na base
            if any(b >= tam_matriz_A for b in vetor_basico):
                print("Problema infactível! Variáveis artificiais permaneceram na base.")
                return None

            # ------------------------------------------------------------------
            # PREPARA SAÍDA PARA FASE 2 (REMOVE ARTIFICIAIS)
            base_final = [b for b in vetor_basico if b < tam_matriz_A]
            matriz_A_final = [linha[:tam_matriz_A] for linha in matriz_A]
            matriz_C_final = coef_originais + [0.0]*num_folgas

            print(f"Base viável para Fase 2: {base_final}")
            print(f"Dimensões: A={len(matriz_A_final)}x{len(matriz_A_final[0])}, C={len(matriz_C_final)}")
            # ------------------------------------------------------------------

            return base_final, matriz_A_final, matriz_b, matriz_C_final

        # Passo 4: Variável que entra (menor custo relativo)
        k = r_N.index(min(r_N))
        entra = vetor_nao_basico[k]
        print(f"Variável que entra na base: x{entra + 1}")

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

        # Atualização da base
        sai = vetor_basico[sai_idx]
        vetor_basico[sai_idx] = entra
        vetor_nao_basico[k] = sai
        iteracao += 1



def fase2(base_inicial, matriz_A, matriz_b, matriz_C):
    # Validação inicial
    if len(matriz_C) != len(matriz_A[0]):
        raise ValueError(f"Dimensão incompatível: matriz_C tem {len(matriz_C)} elementos, mas matriz_A tem {len(matriz_A[0])} colunas")

    numR = len(matriz_b)
    iteracao = 1
    vetor_basico = base_inicial.copy()
    vetor_nao_basico = [j for j in range(len(matriz_A[0])) if j not in vetor_basico]

    while True:
        print(f"\\n--- Iteração {iteracao} ---")
        print("Base:", vetor_basico)

        # Passo 1: Solução básica
        matriz_basica = [[matriz_A[i][j] for j in vetor_basico] for i in range(numR)]
        try:
            B_inv = matriz_inversa(matriz_basica)
            x_B = multiplicar_matrizes(B_inv, [[bi] for bi in matriz_b])
        except Exception as e:
            print("Erro na inversão:", e)
            return None

        # Passo 2: Custos relativos
        c_B = [matriz_C[j] for j in vetor_basico]
        lambda_T = multiplicar_matrizes([c_B], B_inv)
        
        r_N = []
        for j in vetor_nao_basico:
            coluna_j = [[matriz_A[i][j]] for i in range(numR)]
            produto = multiplicar_matrizes(lambda_T, coluna_j)[0][0]
            r_N.append(matriz_C[j] - produto)

        print("Custos relativos (r_N):", [round(r, 6) for r in r_N])

        # Passo 3: Teste de otimalidade
        if all(r >= -1e-10 for r in r_N):
            solucao = [0.0] * len(matriz_A[0])
            for i, idx in enumerate(vetor_basico):
                solucao[idx] = x_B[i][0]
            valor = sum(matriz_C[j] * solucao[j] for j in range(len(matriz_A[0])))
            print("Solução ótima encontrada!")
            return solucao, valor

        # Passo 4: Variável que entra
        k = r_N.index(min(r_N))
        entra = vetor_nao_basico[k]

        # Passo 5: Direção simplex
        y = multiplicar_matrizes(B_inv, [[matriz_A[i][entra]] for i in range(numR)])

        # Passo 6: Variável que sai
        theta_min = float('inf')
        sai_idx = None
        for i in range(numR):
            if y[i][0] > 1e-10:
                theta = x_B[i][0] / y[i][0]
                if theta < theta_min:
                    theta_min = theta
                    sai_idx = i

        if sai_idx is None:
            print("Problema ilimitado!")
            return None

        # Atualização da base
        sai = vetor_basico[sai_idx]
        vetor_basico[sai_idx] = entra
        vetor_nao_basico[k] = sai
        iteracao += 1


def main():
    resultado_fase1 = fase1()
    if resultado_fase1 is None:
        print("Problema infactível na Fase 1")
        return
    
    base_viavel, A, b, c = resultado_fase1
    print(f"Base viável encontrada: {base_viavel}")
    
    resultado_fase2 = fase2(base_viavel, A, b, c)
    if resultado_fase2:
        solucao, valor = resultado_fase2
        print("\nSolução ótima:", solucao)
        print("Valor objetivo:", valor)

    return

if __name__ == "__main__":
    main()