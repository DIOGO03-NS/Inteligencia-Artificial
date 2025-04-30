import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
plt.style.use('seaborn-v0_8')

# Entradas
nivel_sujeira = ctrl.Antecedent(np.arange(0, 11, 1), 'nivel_sujeira')  # 0-10 (limpo a muito sujo)
massa_roupa = ctrl.Antecedent(np.arange(0, 11, 1), 'massa_roupa')      # 0-10 (leve a pesada)
sensibilidade_roupa = ctrl.Antecedent(np.arange(0, 11, 1), 'sensibilidade_roupa')  # 0=fragil a 10=resistente

# Saídas
temperatura = ctrl.Consequent(np.arange(0, 81, 1), 'temperatura')       # 0-80°C
tempo_processo = ctrl.Consequent(np.arange(0, 151, 1), 'tempo_processo') # 0-150 minutos


# Funções de Pertinenscia
# sujeira
nivel_sujeira['baixa'] = fuzz.trimf(nivel_sujeira.universe, [0, 0, 4])   # Até 4 unidades
nivel_sujeira['media'] = fuzz.trimf(nivel_sujeira.universe, [3, 6, 8])   # 3-8 unidades
nivel_sujeira['alta'] = fuzz.trimf(nivel_sujeira.universe, [6, 10, 10]) # Acima de 6

# quantidade de roupa
massa_roupa['leve'] = fuzz.trimf(massa_roupa.universe, [0, 0, 4])      # Até 4kg
massa_roupa['media'] = fuzz.trimf(massa_roupa.universe, [3, 6, 8])     # 3-8kg
massa_roupa['pesada'] = fuzz.trimf(massa_roupa.universe, [6, 10, 10])  # Acima de 6kg

# sensibilidade
sensibilidade_roupa['sensivel'] = fuzz.trimf(sensibilidade_roupa.universe, [0, 0, 4])     # Sedas, rendas
sensibilidade_roupa['pouco_sensivel'] = fuzz.trimf(sensibilidade_roupa.universe, [3, 5, 8])  # Poliéster
sensibilidade_roupa['resistente'] = fuzz.trimf(sensibilidade_roupa.universe, [6, 10, 10])  # Jeans, algodão

# temperatura
temperatura['baixa'] = fuzz.trimf(temperatura.universe, [0, 0, 27])    # Fria/ambiente
temperatura['media'] = fuzz.trimf(temperatura.universe, [20, 34, 45])  # Morna
temperatura['alta'] = fuzz.trimf(temperatura.universe, [40, 55, 70])   # Quente

# tempo
tempo_processo['rapido'] = fuzz.trimf(tempo_processo.universe, [0, 0, 50])    # Rápido (<50min)
tempo_processo['normal'] = fuzz.trimf(tempo_processo.universe, [40, 80, 95])  # Padrão (40-95min)
tempo_processo['lento'] = fuzz.trimf(tempo_processo.universe, [80, 120, 130]) # Demorado (>80min)


# Graficos Funções
# sujeira e aasssa
nivel_sujeira.view(title='Níveis de Sujeira')
plt.suptitle('Classificação da Sujeira', y=1.02)
plt.show()

massa_roupa.view(title='Massa da Roupa')
plt.suptitle('Classificação do Peso', y=1.02)
plt.show()

# configuração de lavagem
temperatura.view(title='Opções de Temperatura')
plt.suptitle('Perfil de Temperatura', y=1.02)
plt.show()

tempo_processo.view(title='Duração do Ciclo')
plt.suptitle('Tempo de Lavagem', y=1.02)
plt.show()

# Regras

regras = [
    # para temperatura
    ctrl.Rule(nivel_sujeira['alta'] & sensibilidade_roupa['resistente'], temperatura['alta'], 
             'Regra 1: Sujeira pesada + tecido resistente → Alta temperatura'),
    
    ctrl.Rule(nivel_sujeira['media'] & (massa_roupa['pesada'] | sensibilidade_roupa['pouco_sensivel']), temperatura['media'],
             'Regra 2: Sujeira média + carga pesada OU tecido pouco sensível → Temperatura média'),
    
    ctrl.Rule(nivel_sujeira['baixa'] & (sensibilidade_roupa['sensivel'] | massa_roupa['pesada']), temperatura['baixa'],
             'Regra 3: Sujeira baixa + tecido sensível OU carga pesada → Baixa temperatura'),

    # para tempo 
    ctrl.Rule(nivel_sujeira['alta'] & sensibilidade_roupa['sensivel'] & massa_roupa['pesada'], tempo_processo['lento'],
             'Regra 4: Trio crítico (sujeira alta + sensível + pesado) → Ciclo longo'),
    
    ctrl.Rule((nivel_sujeira['media'] & sensibilidade_roupa['pouco_sensivel']) | massa_roupa['leve'], tempo_processo['rapido'],
             'Regra 5: Condições médias + pouco sensível OU carga leve → Ciclo rápido'),
    
    ctrl.Rule(nivel_sujeira['alta'] & sensibilidade_roupa['pouco_sensivel'] & massa_roupa['leve'], tempo_processo['rapido'],
             'Regra 6: Sujeira alta + pouco sensível + carga leve → Ciclo rápido'),
    
    ctrl.Rule(nivel_sujeira['baixa'] & sensibilidade_roupa['pouco_sensivel'] & massa_roupa['media'], tempo_processo['normal'],
             'Regra 7: Combinação balanceada → Ciclo normal'),
    
    ctrl.Rule(nivel_sujeira['alta'] & sensibilidade_roupa['resistente'] & massa_roupa['media'], tempo_processo['lento'],
             'Regra 8: Alta sujeira + tecido resistente → Ciclo demorado'),
    
    ctrl.Rule(nivel_sujeira['media'] & sensibilidade_roupa['resistente'] & massa_roupa['media'], tempo_processo['normal'],
             'Regra 9: Parâmetros médios → Ciclo normal'),
    
    ctrl.Rule(nivel_sujeira['media'] & sensibilidade_roupa['resistente'] & massa_roupa['leve'], tempo_processo['rapido'],
             'Regra 10: Carga leve + resistente → Ciclo rápido'),
    
    ctrl.Rule(nivel_sujeira['baixa'] & sensibilidade_roupa['resistente'] & massa_roupa['media'], tempo_processo['rapido'],
             'Regra 11: Pouca sujeira + resistente → Ciclo rápido'),
    
    ctrl.Rule(nivel_sujeira['media'] & sensibilidade_roupa['sensivel'] & massa_roupa['pesada'], tempo_processo['lento'],
             'Regra 12: Sensível + pesado → Ciclo cuidadoso')
]


# Simulação

# Configuração do sistema
sistema_lavadora = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema_lavadora)

# Valores de teste
simulador.input['nivel_sujeira'] = 7.7    # Alto
simulador.input['massa_roupa'] = 6.3      # Médio/Pesado
simulador.input['sensibilidade_roupa'] = 7 # Pouco sensível

# Processamento
simulador.compute()

# Resultados
print(f"""
=== RESULTADO DA LAVAGEM ===
Temperatura ideal: {simulador.output['temperatura']:.1f}°C
Duração do ciclo: {simulador.output['tempo_processo']:.1f} minutos
""")

# Graficos
temperatura.view(sim=simulador)
plt.suptitle('Temperatura Selecionada', y=1.02)
plt.show()

tempo_processo.view(sim=simulador)
plt.suptitle('Duração do Ciclo Calculada', y=1.02)
plt.show()