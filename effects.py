"""
Arquivo de definição dos efeitos e seus multiplicadores.
Contém os efeitos disponíveis no jogo e seus valores de multiplicador.
"""

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

def get_multiplier_value(effect_name):
    """Retorna o valor do multiplicador para um efeito específico."""
    return effect_multipliers.get(effect_name, 0.0)

def get_effects_list():
    """Retorna a lista de todos os efeitos disponíveis."""
    return list(effect_multipliers.keys())

def calculate_total_multiplier(effects):
    """
    Calcula o multiplicador final como a soma dos multiplicadores dos efeitos ativos.
    
    Args:
        effects: Dicionário de efeitos ativos e seus valores
    
    Returns:
        float: O multiplicador total (1.0 + soma dos valores)
    """
    return 1.0 + sum(effects.values())