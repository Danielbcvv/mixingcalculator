"""
Módulo de definição das matérias-primas disponíveis no jogo.
Contém informações sobre as matérias-primas, seus efeitos base e valores.
"""

# Definição das matérias-primas e suas propriedades
RAW_MATERIALS = {
    "OG Kush": {
        "effect": "Calming",
        "value": 35,
        "img_path": "images/og_kush.png"
    },
    "Sour Diesel": {
        "effect": "Refreshing",
        "value": 35,
        "img_path": "images/sour_diesel.png"
    },
    "Green Crack": {
        "effect": "Energizing",
        "value": 35,
        "img_path": "images/green_crack.png"
    },
    "Granddaddy Purple": {
        "effect": "Sedating",
        "value": 35,
        "img_path": "images/granddaddy_purple.png"
    },
    "Meth": {
        "effect": "None",
        "value": 70,
        "img_path": "images/meth.png"
    },
    "Cocaine": {
        "effect": "None",
        "value": 150,
        "img_path": "images/cocaine.png"
    }
}

def get_raw_materials_list():
    """Retorna a lista de todas as matérias-primas disponíveis."""
    return list(RAW_MATERIALS.keys())

def get_raw_material_effect(raw_material_name):
    """Retorna o efeito base de uma matéria-prima específica."""
    if raw_material_name in RAW_MATERIALS:
        return RAW_MATERIALS[raw_material_name].get("effect", "")
    return ""

def get_raw_material_value(raw_material_name):
    """Retorna o valor base de uma matéria-prima específica."""
    if raw_material_name in RAW_MATERIALS:
        return RAW_MATERIALS[raw_material_name].get("value", 0)
    return 0

def get_raw_material_img_path(raw_material_name):
    """Retorna o caminho da imagem de uma matéria-prima específica."""
    if raw_material_name in RAW_MATERIALS:
        return RAW_MATERIALS[raw_material_name].get("img_path", "")
    return ""