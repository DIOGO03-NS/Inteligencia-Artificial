Algoritmo Genético para Evoluir uma String

Este é um algoritmo genético que tenta evoluir uma população de strings até que uma delas corresponda a uma frase-alvo. O algoritmo utiliza os principais conceitos de seleção, crossover e mutação para encontrar a solução.

🧬 Conceitos Utilizados

População inicial: Um conjunto aleatório de strings.

Função de fitness: Mede o quão próxima uma string está da solução.

Seleção: Escolhe os melhores indivíduos para reproduzir (método da roleta).

Crossover: Combina duas strings para criar novas (ponto de corte único).

Mutação: Altera caracteres aleatoriamente para introduzir diversidade.

🚀 Como Funciona

Gera uma população inicial de strings aleatórias.

Avalia o fitness de cada string.

Seleciona os melhores pais (baseado no fitness).

Aplica crossover para criar novos indivíduos.

Aplica mutação para modificar alguns caracteres.

Substitui a população e repete o processo até encontrar a solução.

📌 Estrutura do Código

1. Parâmetros Globais

TARGET = "A frase aqui"  # Frase que queremos evoluir
POPULATION_SIZE = 100      # Quantidade de indivíduos na população
MUTATION_RATE = 0.01       # Probabilidade de um caractere ser mutado

2. Função de Fitness

def fitness(individuo):
    return sum(1 for a, b in zip(individuo, TARGET) if a == b)

Compara cada caractere da string com a frase-alvo e conta quantos estão corretos.

3. Seleção (Roleta)

def selecionar_pais(populacao):
    soma_fit = sum(fitness(ind) for ind in populacao)
    pais = []
    for _ in range(2):
        sorteio = random.uniform(0, soma_fit)
        acumulador = 0
        for ind in populacao:
            acumulador += fitness(ind)
            if acumulador >= sorteio:
                pais.append(ind)
                break
    return pais

Escolhe dois pais com base na probabilidade proporcional ao fitness.

4. Crossover (Ponto de Corte Único)

def crossover(pai1, pai2):
    ponto = random.randint(1, len(TARGET)-1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

Escolhe um ponto de corte aleatório e combina os genes dos pais para gerar dois filhos.

5. Mutação

def mutacao(individuo):
    novo = ""
    for ch in individuo:
        if random.random() < MUTATION_RATE:
            novo += chr(random.randint(32, 126))
        else:
            novo += ch
    return novo

Cada caractere tem uma chance de ser modificado aleatoriamente.

6. Algoritmo Principal

populacao = ["".join(random.choices(chr(random.randint(32, 126)) for _ in range(len(TARGET)))) for _ in range(POPULATION_SIZE)]

geracao = 0
while True:
    populacao = sorted(populacao, key=fitness, reverse=True)
    
    if populacao[0] == TARGET:
        print(f"Solução encontrada na geração {geracao}: {populacao[0]}")
        break
    
    nova_populacao = []
    for _ in range(POPULATION_SIZE // 2):
        pai1, pai2 = selecionar_pais(populacao)
        filho1, filho2 = crossover(pai1, pai2)
        nova_populacao.extend([mutacao(filho1), mutacao(filho2)])
    
    populacao = nova_populacao
    geracao += 1

Gera uma população inicial aleatória.

Ordena por melhor fitness.

Se encontrou a solução, para.

Caso contrário, cria uma nova geração aplicando seleção, crossover e mutação.

Repete até encontrar a string-alvo.