import random
import time

POP_SIZE = 100         
MUTATION_RATE = 0.1    # Taxa de mutação (10%)
TARGET = "O rato roeu a roupa do rei de roma" 

# gera opções aleatorias
def gerar_individuo():
    return ''.join(chr(random.randint(32, 126)) for _ in range(len(TARGET)))

# achar o fitness
def fitness(individuo):
    return sum(1 for i, ch in enumerate(individuo) if ch == TARGET[i])

# seleção -> Roleta
def selecionar_pais(populacao):
    soma_fit = sum(fitness(ind) for ind in populacao)
    pais = []
    for i in range(2):
        sorteio = random.uniform(0, soma_fit)
        acumulador = 0
        for ind in populacao:
            acumulador += fitness(ind)
            if acumulador >= sorteio:
                pais.append(ind)
                break
    return pais

# crossover
def crossover(pai1, pai2):
    ponto = random.randint(1, len(TARGET)-1)
    filho1 = pai1[:ponto] + pai2[ponto:]
    filho2 = pai2[:ponto] + pai1[ponto:]
    return filho1, filho2

# mutação
def mutacao(individuo):
    novo = ""
    for i, ch in enumerate(individuo):
        if random.random() < MUTATION_RATE:
            if ch == TARGET[i]:  # menor chance de mudar
                novo += ch if random.random() > 0.9 else chr(random.randint(32, 126))
            else:
                # muda caracteres perto do alvo
                novo += chr(random.randint(ord(TARGET[i]) - 2, ord(TARGET[i]) + 2))
        else:
            novo += ch
    return novo

# inicialização da população
populacao = [gerar_individuo() for i in range(POP_SIZE)]

# cronometrar
inicio = time.time()
geracao = 0

# evolução 
while True:
    # avaliação
    fitnesses = [fitness(ind) for ind in populacao]
    melhor_fit = max(fitnesses)
    melhor_ind = populacao[fitnesses.index(melhor_fit)]
    print(f"Geração {geracao}: Melhor fitness = {melhor_fit}, Indivíduo = {melhor_ind}")
    
    # se atingir o target 
    if melhor_fit == len(TARGET):
        fim = time.time()
        print(f"Solução ótima encontrada em {geracao} gerações e {fim - inicio:.4f} segundos!")
        break

    nova_pop = []
    # preserva os melhores
    elite = melhor_ind
    nova_pop.append(elite)
    
    # cria nova população
    while len(nova_pop) < POP_SIZE:
        pai1, pai2 = selecionar_pais(populacao)
        filho1, filho2 = crossover(pai1, pai2)
        nova_pop.append(mutacao(filho1))
        if len(nova_pop) < POP_SIZE:
            nova_pop.append(mutacao(filho2))
    populacao = nova_pop

    geracao+=1

# solução não encontrada
if melhor_fit < len(TARGET):
    fim = time.time()
    print(f"Tempo final: {fim - inicio:.4f} segundos. Solução não encontrada após {GENERATIONS} gerações.")
