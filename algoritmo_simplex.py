def ler_arquivo(nome_arquivo="funcao.txt"):
    """Lê o arquivo e retorna suas linhas."""
    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
        return [linha.strip() for linha in arquivo.readlines()]

def identificar_tipo_funcao(linha):
    """Verifica se a função é de maximização ou minimização."""
    return linha.lower().startswith("max")

def extrair_coeficientes(linha):
    """Extrai os coeficientes da função objetivo."""
    linha = linha[7:].strip()  # Remove "max z =" ou "min z =" e espaços extras
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
    """Extrai a matriz de coeficientes, o vetor de resultados e adiciona variáveis de folga/excesso."""
    matriz_coef = []
    vetor_resultados = []
    num_variaveis = 0
    num_folga = 0
    restricoes_processadas = []

    for linha in linhas[1:]:  # Pula a função objetivo
        coef = ""
        restricao = []
        partes = linha.split()

        # Identificar o termo independente (último elemento da equação)
        resultado = int(partes[-1])
        vetor_resultados.append(resultado)

        # Identificar o tipo da restrição
        if ">=" in linha:
            tipo_restricao = ">="
        elif "<=" in linha:
            tipo_restricao = "<="
        else:
            tipo_restricao = "="

        # Processar coeficientes antes do sinal (>=, <=, =)
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

        num_variaveis = max(num_variaveis, len(restricao))  # Atualiza o número de variáveis

        # Variáveis de folga ou excesso
        folga = [0] * num_folga  # Mantém folgas anteriores
        if tipo_restricao == "<=":
            folga.append(1)  # Variável de folga positiva
        elif tipo_restricao == ">=":
            folga.append(-1)  # Variável de excesso negativa
        elif tipo_restricao == "=":
            folga.append(0)  # Sem variável de folga/excesso

        num_folga += 1
        restricao.extend(folga)  # Adiciona folgas à restrição
        restricoes_processadas.append(restricao)

    # Ajustar o tamanho de cada restrição para garantir alinhamento das colunas
    num_total_variaveis = num_variaveis + num_folga
    for restricao in restricoes_processadas:
        while len(restricao) < num_total_variaveis:
            restricao.append(0)
        matriz_coef.append(restricao)

    return matriz_coef, vetor_resultados

def main():
    linhas = ler_arquivo()
    
    tipo_maximizacao = identificar_tipo_funcao(linhas[0])  # Identifica max ou min
    coef_funcao_objetivo = extrair_coeficientes(linhas[0])  # Coeficientes da função objetivo
    matriz_restricoes, vetor_resultados = extrair_restricoes(linhas)  # Matriz e resultados

    print("Maximizacao:", tipo_maximizacao)
    print("Coeficientes da Funcao Objetivo:", coef_funcao_objetivo)  # Sem variáveis de folga
    print("Matriz de Coeficientes das Restricowes:")
    for linha in matriz_restricoes:
        print(linha)
    print("Vetor de Resultados:", vetor_resultados)

if __name__ == "__main__":
    main()
