"""
Arquivo de definição dos itens, seus preços e regras de modificação.
Contém todos os itens disponíveis no jogo, seus efeitos base e 
regras de transformação de efeitos quando combinados.
"""

# Adicionando os preços dos itens
item_prices = {
    "Cuke": 2,
    "Flu Medicine": 5,
    "Gasoline": 5,
    "Donut": 3,
    "Energy Drink": 6,
    "Mouth Wash": 4,
    "Motor Oil": 6,
    "Banana": 2,
    "Chili": 7,
    "Iodine": 8,
    "Paracetamol": 3,
    "Viagra": 4,
    "Horse Semen": 9,
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

def get_item_price(item_name):
    """Retorna o preço de um item específico."""
    return item_prices.get(item_name, 0)

def get_item_effect(item_name):
    """Retorna o efeito base de um item específico."""
    if item_name in items:
        return items[item_name].get("effect", "")
    return ""

def get_item_rules(item_name):
    """Retorna as regras de transformação de um item específico."""
    if item_name in items:
        return items[item_name].get("rules", {})
    return {}

def get_all_items():
    """Retorna a lista de todos os itens disponíveis."""
    return list(items.keys())

def calculate_total_cost(item_combination):
    """
    Calcula o custo total de uma combinação de itens.
    
    Args:
        item_combination: Lista de nomes de itens
    
    Returns:
        float: O custo total da combinação
    """
    return sum(item_prices.get(item, 0) for item in item_combination)