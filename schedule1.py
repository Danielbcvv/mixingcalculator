import itertools
import random
import time
from typing import Dict, List, Set, Tuple

# Definindo os efeitos e seus multiplicadores
effect_multipliers = {
    "Anti-Gravity": 0.54,
    "Athletic": 0.32,
    "Balding": 0.30,
    "Bright-Eyed": 0.40,
    "Calming": 0.10,
    "Calorie-Dense": 0.28,
    "Cyclopean": 0.56,
    "Disorienting": 0.00,
    "Electrifying": 0.50,
    "Energizing": 0.22,
    "Euphoric": 0.18,
    "Explosive": 0.00,
    "Focused": 0.16,
    "Foggy": 0.36,
    "Gingeritis": 0.20,
    "Glowing": 0.48,
    "Jennerising": 0.42,
    "Laxative": 0.00,
    "Long Faced": 0.52,
    "Munchies": 0.12,
    "Paranoia": 0.00,
    "Refreshing": 0.14,
    "Schizophrenia": 0.00,
    "Sedating": 0.26,
    "Seizure-Inducing": 0.00,
    "Shrinking": 0.60,
    "Slippery": 0.34,
    "Smelly": 0.00,
    "Sneaky": 0.24,
    "Spicy": 0.38,
    "Thought-Provoking": 0.44,
    "Toxic": 0.00,
    "Tropic Thunder": 0.46,
    "Zombifying": 0.58
}

# Adicionando os preços dos itens
item_prices = {
    "Cuke": 2,
    "Flu Medicine": 5,
    "Gasoline": 5,
    "Donut": 3,
    "Energy Drink": 6,  # Corrigido de "Energetic Drink" para "Energy Drink" para corresponder às chaves no dicionário 'items'
    "Mouth Wash": 4,
    "Motor Oil": 6,
    "Banana": 2,
    "Chili": 7,
    "Iodine": 8,
    "Paracetamol": 3,  # Corrigido de "Parecetamol" para "Paracetamol" para corresponder às chaves no dicionário 'items'
    "Viagra": 4,
    "Horse Semen": 9,  # Corrigido de "House Semen" para "Horse Semen" para corresponder às chaves no dicionário 'items'
    "Mega Bean": 7,
    "Addy": 9,
    "Battery": 8
}

# Definindo os itens, seus efeitos e regras de modificação
items = {
    "Cuke": {
        "effect": "Energizing",
        "rules": {
            "Toxic": "Euphoric",
            "Slippery": "Munchies",
            "Sneaky": "Paranoia",
            "Foggy": "Cyclopean",
            "Gingeritis": "Thought-Provoking",
            "Munchies": "Athletic",
            "Euphoric": "Laxative"
        }
    },
    "Flu Medicine": {
        "effect": "Sedating",
        "rules": {
            "Calming": "Bright-Eyed",
            "Athletic": "Munchies",
            "Thought-Provoking": "Gingeritis",
            "Cyclopean": "Foggy",
            "Munchies": "Slippery",
            "Laxative": "Euphoric",
            "Euphoric": "Toxic",
            "Focused": "Calming",
            "Electrifying": "Refreshing",
            "Shrinking": "Paranoia"
        }
    },
    "Gasoline": {
        "effect": "Toxic",
        "rules": {
            "Gingeritis": "Smelly",
            "Jennerising": "Sneaky",
            "Sneaky": "Tropic Thunder",
            "Munchies": "Sedating",
            "Energizing": "Euphoric",
            "Euphoric": "Energizing",
            "Laxative": "Foggy",
            "Disorienting": "Glowing",
            "Paranoia": "Calming",
            "Electrifying": "Disorienting",
            "Shrinking": "Focused"
        }
    },
    "Donut": {
        "effect": "Calorie-Dense",
        "rules": {
            "Calorie-Dense": "Explosive",
            "Balding": "Sneaky",
            "Anti-Gravity": "Slippery",
            "Jennerising": "Gingeritis",
            "Focused": "Euphoric",
            "Shrinking": "Energizing"
        }
    },
    "Energy Drink": {
        "effect": "Athletic",
        "rules": {
            "Sedating": "Munchies",
            "Euphoric": "Energizing",
            "Spicy": "Euphoric",
            "Tropic Thunder": "Sneaky",
            "Glowing": "Disorienting",
            "Foggy": "Laxative",
            "Disorienting": "Electrifying",
            "Schizophrenia": "Balding",
            "Focused": "Shrinking"
        }
    },
    "Mouth Wash": {
        "effect": "Balding",
        "rules": {
            "Calming": "Anti-Gravity",
            "Calorie-Dense": "Sneaky",
            "Explosive": "Sedating",
            "Focused": "Jennerising"
        }
    },
    "Motor Oil": {
        "effect": "Slippery",
        "rules": {
            "Energizing": "Munchies",
            "Foggy": "Toxic",
            "Euphoric": "Sedating",
            "Paranoia": "Anti-Gravity",
            "Munchies": "Schizophrenia"
        }
    },
    "Banana": {
        "effect": "Gingeritis",
        "rules": {
            "Energizing": "Thought-Provoking",
            "Calming": "Sneaky",
            "Toxic": "Smelly",
            "Long Faced": "Refreshing",
            "Cyclopean": "Thought-Provoking",
            "Disorienting": "Focused",
            "Focused": "Seizure-Inducing",
            "Paranoia": "Jennerising",
            "Smelly": "Anti-Gravity"
        }
    },
    "Chili": {
        "effect": "Spicy",
        "rules": {
            "Athletic": "Euphoric",
            "Anti-Gravity": "Tropic Thunder",
            "Sneaky": "Bright-Eyed",
            "Munchies": "Toxic",
            "Laxative": "Long Faced",
            "Shrinking": "Refreshing"
        }
    },
    "Iodine": {
        "effect": "Jennerising",
        "rules": {
            "Calming": "Balding",
            "Toxic": "Sneaky",
            "Foggy": "Paranoia",
            "Calorie-Dense": "Gingeritis",
            "Euphoric": "Seizure-Inducing",
            "Refreshing": "Thought-Provoking"
        }
    },
    "Paracetamol": {
        "effect": "Sneaky",
        "rules": {
            "Energizing": "Paranoia",
            "Calming": "Slippery",
            "Toxic": "Tropic Thunder",
            "Spicy": "Bright-Eyed",
            "Glowing": "Toxic",
            "Foggy": "Calming",
            "Munchies": "Anti-Gravity",
            "Paranoia": "Balding",
            "Electrifying": "Athletic",
            "Focused": "Gingeritis"
        }
    },
    "Viagra": {
        "effect": "Tropic Thunder",
        "rules": {
            "Athletic": "Sneaky",
            "Euphoric": "Bright-Eyed",
            "Laxative": "Calming",
            "Disorienting": "Toxic"
        }
    },
    "Horse Semen": {
        "effect": "Long Faced",
        "rules": {
            "Anti-Gravity": "Calming",
            "Gingeritis": "Refreshing",
            "Thought-Provoking": "Electrifying"
        }
    },
    "Mega Bean": {
        "effect": "Foggy",
        "rules": {
            "Energizing": "Cyclopean",
            "Calming": "Glowing",
            "Sneaky": "Calming",
            "Jennerising": "Paranoia",
            "Athletic": "Laxative",
            "Slippery": "Toxic",
            "Thought-Provoking": "Energizing",
            "Seizure-Inducing": "Focused",
            "Focused": "Disorienting",
            "Shrinking": "Electrifying"
        }
    },
    "Addy": {
        "effect": "Thought-Provoking",
        "rules": {
            "Sedating": "Gingeritis",
            "Long Faced": "Electrifying",
            "Glowing": "Refreshing",
            "Foggy": "Energizing",
            "Explosive": "Euphoric"
        }
    },
    "Battery": {
        "effect": "Bright-Eyed",
        "rules": {
            "Munchies": "Tropic Thunder",
            "Euphoric": "Zombifying",
            "Electrifying": "Euphoric",
            "Laxative": "Calorie-Dense",
            "Cyclopean": "Glowing",
            "Shrinking": "Munchies"
        }
    }
}

def apply_item_effects(selected_items: List[str], initial_effects: Dict[str, float] = None) -> Dict[str, float]:
    """
    Aplica os efeitos dos itens selecionados na ordem correta e retorna
    o conjunto final de efeitos ativos e seus multiplicadores.
    Com limite de 8 efeitos simultâneos.
    
    Args:
        selected_items: Lista de itens na ordem em que serão aplicados
        initial_effects: Dicionário opcional de efeitos iniciais já presentes
    """
    # Inicializa com os efeitos iniciais, se fornecidos
    active_effects = initial_effects.copy() if initial_effects else {}
    MAX_EFFECTS = 8  # Limite máximo de efeitos simultâneos
    
    for item_name in selected_items:
        # Adiciona o efeito do item apenas se ainda não alcançamos o limite de efeitos
        item = items[item_name]
        effect = item["effect"]
        
        # Se já temos 8 efeitos e este efeito não está entre eles, não adicionamos
        if len(active_effects) >= MAX_EFFECTS and effect not in active_effects:
            # Não adiciona o efeito, mas ainda aplica as regras de transformação
            pass
        else:
            # Adiciona o efeito normalmente
            active_effects[effect] = effect_multipliers[effect]
        
        # Aplica as regras de modificação (isso acontece independentemente de ter adicionado o efeito)
        effects_to_change = {}
        for current_effect, new_effect in item["rules"].items():
            # Não aplicar a regra ao próprio efeito que acabamos de adicionar
            if current_effect in active_effects and current_effect != effect:
                effects_to_change[current_effect] = new_effect
        
        # Aplica as mudanças
        for old_effect, new_effect in effects_to_change.items():
            del active_effects[old_effect]
            active_effects[new_effect] = effect_multipliers[new_effect]
    
    return active_effects

def debug_apply_item_effects(selected_items: List[str], initial_effects: Dict[str, float] = None) -> Dict[str, float]:
    """
    Versão detalhada da função apply_item_effects que imprime cada passo do processo.
    Com limite de 8 efeitos simultâneos.
    """
    # Inicializa com os efeitos iniciais, se fornecidos
    active_effects = initial_effects.copy() if initial_effects else {}
    MAX_EFFECTS = 8  # Limite máximo de efeitos simultâneos
    
    print(f"Efeitos iniciais: {active_effects}")
    
    for i, item_name in enumerate(selected_items, 1):
        print(f"\nPasso {i}: Aplicando item '{item_name}'")
        item = items[item_name]
        effect = item["effect"]
        
        # Verifica se já atingimos o limite de efeitos
        if len(active_effects) >= MAX_EFFECTS and effect not in active_effects:
            print(f"  Limite de {MAX_EFFECTS} efeitos atingido! O efeito {effect} não será adicionado.")
            print(f"  Efeitos atuais: {active_effects}")
        else:
            print(f"  Adicionando efeito: {effect} (+{effect_multipliers[effect]})")
            active_effects[effect] = effect_multipliers[effect]
            print(f"  Efeitos após adicionar {effect}: {active_effects}")
        
        # Identifica quais regras serão aplicadas
        effects_to_change = {}
        print("  Verificando regras de modificação:")
        for current_effect, new_effect in item["rules"].items():
            if current_effect in active_effects and current_effect != effect:
                print(f"    Regra ativa: {current_effect} -> {new_effect}")
                effects_to_change[current_effect] = new_effect
            else:
                if current_effect not in active_effects:
                    print(f"    Regra ignorada (efeito não presente): {current_effect} -> {new_effect}")
                elif current_effect == effect:
                    print(f"    Regra ignorada (é o efeito que acabamos de adicionar): {current_effect} -> {new_effect}")
        
        # Aplica as mudanças
        for old_effect, new_effect in effects_to_change.items():
            print(f"  Substituindo: {old_effect} -> {new_effect} (+{effect_multipliers[new_effect]})")
            del active_effects[old_effect]
            active_effects[new_effect] = effect_multipliers[new_effect]
        
        print(f"  Efeitos ativos após aplicar o item {item_name}: {active_effects}")
        print(f"  Número de efeitos ativos: {len(active_effects)}")
    
    print("\nEfeitos finais:")
    for effect, value in sorted(active_effects.items(), key=lambda x: x[1], reverse=True):
        print(f"- {effect}: +{value:.2f}")
    
    return active_effects

def calculate_multiplier(effects: Dict[str, float]) -> float:
    """
    Calcula o multiplicador final como a soma dos multiplicadores dos efeitos ativos.
    """
    return 1.0 + sum(effects.values())

def calculate_total_cost(combination: List[str]) -> float:
    """
    Calcula o custo total da combinação de itens.
    """
    return sum(item_prices[item] for item in combination)

def evaluate_combination(combination: List[str], initial_effects: Dict[str, float] = None) -> Tuple[float, Dict[str, float], float]:
    """
    Avalia uma combinação de itens e retorna o multiplicador, os efeitos finais e o custo total.
    """
    effects = apply_item_effects(combination, initial_effects)
    multiplier = calculate_multiplier(effects)
    cost = calculate_total_cost(combination)
    return multiplier, effects, cost

def generate_random_combination(available_items, combo_size):
    """
    Gera uma combinação aleatória de itens com o tamanho especificado,
    considerando apenas os itens disponíveis e permitindo repetições.
    """
    return [random.choice(available_items) for _ in range(combo_size)]

def mutate_combination(combination, available_items, mutation_rate=0.3):
    """
    Aplica mutação a uma combinação, alterando itens com base na taxa de mutação.
    Permite repetição de itens.
    """
    result = combination.copy()
    
    # Determina quantos itens serão mutados com base na taxa de mutação
    num_mutations = max(1, int(len(combination) * mutation_rate * random.uniform(0.5, 1.5)))
    
    # Índices dos itens a serem mutados
    indices_to_mutate = random.sample(range(len(combination)), min(num_mutations, len(combination)))
    
    for idx in indices_to_mutate:
        # Seleciona um novo item aleatório da lista de disponíveis (permitindo repetições)
        result[idx] = random.choice(available_items)
    
    # 50% de chance de embaralhar a ordem após a mutação
    if random.random() < 0.5:
        random.shuffle(result)
    
    return result

def crossover(parent1, parent2, available_items):
    """
    Realiza um crossover entre dois pais para criar um filho.
    Implementa diferentes estratégias de crossover aleatoriamente.
    Permite repetições de itens.
    """
    # Escolhe aleatoriamente uma estratégia de crossover
    strategy = random.choice(["one_point", "two_point", "uniform"])
    
    child = []
    
    if strategy == "one_point":
        # Crossover de um ponto
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
                
    elif strategy == "two_point":
        # Crossover de dois pontos
        if len(parent1) >= 3:
            point1, point2 = sorted(random.sample(range(1, len(parent1)), 2))
            child = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        else:
            # Fallback para crossover uniforme em caso de combinações muito pequenas
            strategy = "uniform"
    
    if strategy == "uniform" or len(child) < len(parent1):
        # Crossover uniforme ou fallback
        child = []
        
        for i in range(len(parent1)):
            # 50% de chance de pegar do parent1 ou parent2
            if random.random() < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
    
    # Verifica se o filho tem o tamanho correto
    while len(child) < len(parent1):
        child.append(random.choice(available_items))
    
    # Trunca se por algum motivo o filho ficou maior
    if len(child) > len(parent1):
        child = child[:len(parent1)]
    
    # Embaralha a ordem com 50% de chance
    if random.random() < 0.5:
        random.shuffle(child)
    
    return child

def tournament_selection(population, tournament_size=3, base_value=100):
    """
    Seleciona um indivíduo da população usando seleção por torneio.
    Considera o lucro: (base_value * multiplicador) - custo
    
    Args:
        population: Lista de tuplas (combinação, multiplicador, efeitos, custo)
        tournament_size: Tamanho do torneio
        base_value: Valor base para cálculo do lucro
    """
    tournament = random.sample(population, min(tournament_size, len(population)))
    
    # Calcula o lucro para cada indivíduo
    fitness_scores = []
    
    for ind in tournament:
        mult = ind[1]
        cost = ind[3]
        
        # Lucro = (base_value * multiplicador) - custo
        profit = (base_value * mult) - cost
        fitness_scores.append((ind, profit))
    
    # Retorna o indivíduo com maior lucro
    return max(fitness_scores, key=lambda x: x[1])[0]

def find_best_combination(initial_effects: Dict[str, float] = None, 
                          time_limit_seconds: int = 30, 
                          combo_size: int = 8,
                          max_perms_to_test: int = 5000,
                          banned_items: List[str] = None,
                          cost_weight: float = 0.3,
                          base_value: float = 100):
    """
    Encontra a melhor combinação de itens que maximize o lucro,
    calculado como (base_value * multiplicador) - custo.
    
    Args:
        initial_effects: Dicionário de efeitos iniciais já presentes
        time_limit_seconds: Limite de tempo em segundos para a busca
        combo_size: Número de itens a serem selecionados
        max_perms_to_test: Número máximo de permutações a testar na fase final
        banned_items: Lista de itens que não podem ser usados
        cost_weight: Não utilizado mais, mantido para compatibilidade
        base_value: Valor base usado no cálculo do lucro
    """
    # Remove os itens banidos da lista de itens disponíveis
    all_items = list(items.keys())
    banned_items = banned_items or []
    available_items = [item for item in all_items if item not in banned_items]
    
    if len(available_items) < combo_size:
        print(f"Aviso: O tamanho da combinação ({combo_size}) é maior que o número de itens disponíveis ({len(available_items)}).")
        print(f"Ajustando o tamanho da combinação para {len(available_items)}.")
        combo_size = len(available_items)
    
    best_multiplier = 0.0
    best_combination = []
    best_effects = {}
    best_cost = float('inf')
    best_profit = float('-inf')  # Rastrear o melhor lucro
    
    start_time = time.time()
    
    # Parâmetros do algoritmo genético mais aleatórios
    population_size = random.randint(200, 800)
    num_generations = 10000  # Limite máximo, será limitado pelo tempo
    base_mutation_rate = random.uniform(0.1, 0.8)
    tournament_size = random.randint(2, 8)
    
    print(f"Tamanho da população: {population_size}")
    print(f"Taxa base de mutação: {base_mutation_rate:.2f}")
    print(f"Tamanho do torneio: {tournament_size}")
    print(f"Valor base para cálculo do lucro: ${base_value:.2f}")
    
    # Inicializa a população com combinações aleatórias
    population = []
    for _ in range(population_size):
        combo = generate_random_combination(available_items, combo_size)
        mult, effects, cost = evaluate_combination(combo, initial_effects)
        profit = (base_value * mult) - cost  # Cálculo do lucro
        population.append((combo, mult, effects, cost, profit))
    
    # Ordena a população pelo lucro
    population.sort(key=lambda x: x[4], reverse=True)
    
    # Acompanha o melhor resultado
    best_combination, best_multiplier, best_effects, best_cost, best_profit = population[0]
    print(f"Inicial: Multiplicador = {best_multiplier:.2f}, Custo = ${best_cost:.2f}, Lucro = ${best_profit:.2f}")
    
    # Evolução da população
    for gen in range(num_generations):
        # Verifica se o tempo limite foi atingido
        if time.time() - start_time > time_limit_seconds:
            print(f"Limite de tempo ({time_limit_seconds}s) atingido após {gen} gerações.")
            break
        
        # Exibe progresso a cada 10 gerações
        if gen % 10 == 0:
            print(f"Geração {gen}/{num_generations}: Melhor = {best_multiplier:.2f}, Custo = ${best_cost:.2f}, Lucro = ${best_profit:.2f}")
        
        # Cria nova população
        new_population = []
        
        # Elitismo: mantém os melhores indivíduos da população (percentual variável)
        elite_size = max(1, int(population_size * random.uniform(0.05, 0.15)))
        new_population.extend(population[:elite_size])
        
        # Adiciona variação na taxa de mutação ao longo do tempo
        current_mutation_rate = base_mutation_rate * (1 - gen / (2 * num_generations))
        
        # Crossover e mutação para o resto da população
        while len(new_population) < population_size:
            # Seleção de pais pelo método de torneio
            parent1 = tournament_selection(population, tournament_size, base_value)
            parent2 = tournament_selection(population, tournament_size, base_value)
            
            # Crossover
            child_combo = crossover(parent1[0], parent2[0], available_items)
            
            # Mutação com taxa variável
            if random.random() < current_mutation_rate:
                child_combo = mutate_combination(child_combo, available_items, current_mutation_rate)
            
            # Avalia o filho
            mult, effects, cost = evaluate_combination(child_combo, initial_effects)
            profit = (base_value * mult) - cost  # Cálculo do lucro
            new_population.append((child_combo, mult, effects, cost, profit))
            
            # Atualiza o melhor resultado se necessário com base no lucro
            if profit > best_profit:
                best_multiplier = mult
                best_combination = child_combo.copy()
                best_effects = effects.copy()
                best_cost = cost
                best_profit = profit
                print(f"Novo melhor: Multiplicador = {best_multiplier:.2f}, Custo = ${best_cost:.2f}, Lucro = ${best_profit:.2f}")
        
        # Substitui a população antiga pela nova
        population = sorted(new_population, key=lambda x: x[4], reverse=True)
        
        # Introduz diversidade aleatória a cada N gerações
        if gen % 20 == 0 and gen > 0:
            diversity_count = max(1, int(population_size * 0.1))
            for _ in range(diversity_count):
                random_combo = generate_random_combination(available_items, combo_size)
                mult, effects, cost = evaluate_combination(random_combo, initial_effects)
                profit = (base_value * mult) - cost
                # Substitui um dos piores
                if len(population) > 0:
                    population[-1] = (random_combo, mult, effects, cost, profit)
            
            # Reordena após adicionar diversidade
            population.sort(key=lambda x: x[4], reverse=True)
    
    # Fase final: refina a melhor combinação encontrada
    print("\nRefinando a melhor solução...")
    
    # Limita o número de permutações a testar
    total_possible_perms = len(list(itertools.permutations(best_combination)))
    perms_to_test = min(max_perms_to_test, total_possible_perms)
    
    if perms_to_test > 0:
        if total_possible_perms <= max_perms_to_test:
            permutations = list(itertools.permutations(best_combination))
        else:
            permutations = random.sample(list(itertools.permutations(best_combination)), perms_to_test)
        
        print(f"Testando {perms_to_test} permutações de {total_possible_perms} possíveis")
        
        for i, perm in enumerate(permutations):
            # Verifica se o tempo limite foi atingido
            if time.time() - start_time > time_limit_seconds:
                print(f"Refinamento interrompido após {i}/{perms_to_test} permutações.")
                break
            
            if i % 500 == 0 and i > 0:
                print(f"Testando permutação {i}/{perms_to_test}")
            
            mult, effects, cost = evaluate_combination(perm, initial_effects)
            profit = (base_value * mult) - cost  # Cálculo do lucro
            
            # Atualiza o melhor resultado se necessário
            if profit > best_profit:
                best_multiplier = mult
                best_combination = list(perm)
                best_effects = effects.copy()
                best_cost = cost
                best_profit = profit
                print(f"Refinamento: Novo melhor = {best_multiplier:.2f}, Custo = ${best_cost:.2f}, Lucro = ${best_profit:.2f}")
    
    elapsed_time = time.time() - start_time
    print(f"\nTempo total de execução: {elapsed_time:.2f} segundos")
    
    return best_combination, best_multiplier, best_effects, best_cost, best_profit

def optimize(initial_effects=None, time_limit_seconds=30, combo_size=8, 
            max_perms_to_test=5000, banned_items=None, cost_weight=0.3, base_value=100, verbose=True):
    """
    Executa o processo de otimização e exibe os resultados.
    
    Args:
        initial_effects: Dicionário de efeitos iniciais já presentes
        time_limit_seconds: Limite de tempo em segundos para a busca
        combo_size: Número de itens a serem selecionados
        max_perms_to_test: Número máximo de permutações a testar na fase final
        banned_items: Lista de itens que não podem ser usados
        cost_weight: Não mais utilizado, mantido para compatibilidade
        base_value: Valor base usado no cálculo do lucro
    """
    if initial_effects:
        print(f"Iniciando otimização com os efeitos iniciais: {initial_effects}")
    else:
        print("Iniciando otimização sem efeitos iniciais...")
    
    if banned_items:
        print(f"Itens banidos: {banned_items}")
    else:
        print("Nenhum item está banido.")
    
    print(f"Limite de tempo: {time_limit_seconds} segundos")
    print(f"Tamanho da combinação: {combo_size} itens")
    print(f"Máximo de permutações a testar: {max_perms_to_test}")
    print(f"Valor base para cálculo do lucro: ${base_value:.2f}")
    
    best_combination, best_multiplier, best_effects, best_cost, best_profit = find_best_combination(
        initial_effects=initial_effects,
        time_limit_seconds=time_limit_seconds,
        combo_size=combo_size,
        max_perms_to_test=max_perms_to_test,
        banned_items=banned_items,
        cost_weight=cost_weight,
        base_value=base_value
    )
    
    print("\n===== RESULTADO FINAL =====")
    print(f"Melhor multiplicador: {best_multiplier:.2f}")
    print(f"Custo total: ${best_cost:.2f}")
    print(f"Lucro estimado: ${best_profit:.2f} (Base ${base_value:.2f} * Multiplicador {best_multiplier:.2f} - Custo ${best_cost:.2f})")
    
    print("\nMelhor combinação (na ordem):")
    for i, item in enumerate(best_combination, 1):
        print(f"{i}. {item} (${item_prices[item]})")
    
    print("\nEfeitos finais ativos:")
    # Esta é a parte que precisa ser corrigida
    # Ordenando os efeitos pelo valor multiplicador, em ordem decrescente
    for effect, value in sorted(best_effects.items(), key=lambda x: x[1], reverse=True):
        print(f"- {effect}: +{value:.2f}")
    
    return best_combination, best_multiplier, best_effects, best_cost, best_profit

# Exemplo de uso
if __name__ == "__main__":
    # Parâmetros configuráveis
    initial_effects = { "Energizing": 0.22}  #Efeitos iniciais (opcional) Exemplo: {"Shrinking": 0.60, "Zombifying": 0.58}
    banned_items = ["Horse Semen"]     # Itens banidos (opcional) Exemplo ["Gasoline", "Horse Semen", "Addy"]
    time_limit = 300       # Tempo limite em segundos
    combo_size = 8        # Tamanho da combinação
    perms_to_test = 40000  # Máximo de permutações a testar
    cost_weight = 0.03     # Peso do custo no fitness (não mais utilizado)
    base_value = 43      # Valor base para cálculo do lucro
    
    # Executa a otimização
    optimize(
        initial_effects=initial_effects,
        banned_items=banned_items,
        time_limit_seconds=time_limit,
        combo_size=combo_size,
        max_perms_to_test=perms_to_test,
        cost_weight=cost_weight,
        base_value=base_value
    )