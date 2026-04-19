
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data/elden-ring-data')
CHROMA_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'chroma_db')
COLLECTION_NAME = "elden_ring"


"""
Config to retreive desired fields for each category
"""
field_config = {
    'Ammos' : ['name', 'description', 'ammo_type', 'attack_Power', 'passive_effect'],
    'Armors': ['name','description','armor_class','damage_Negation','resistance','weight'],
    'Ashes' : ['name','description','affinity','skill'],
    'Bosses' : ['name','region','description','location','drops','healthPoints'],
    'Classes' : ['name','description','starting_stats'],
    'Creatures' : ['name','description','location','drops'],
    'Incantations' : ['name','description','type','cost','slots','effects','required_Attributes'],
    'Items' : ['name','description','item_type','effect'],
    'Locations' : ['name','region','description'],
    'Npcs' : ['name','quote','location','role'],
    'Shields' : ['name','description','attack','defence','scales_With','required_Attributes','shield_class','weight'],
    'Sorceries' : ['name','description','type','cost','slots','effects','required_Attributes'],
    'Spirits' : ['name','description','fpCost','hpCost','effect'],
    'Talismans' : ['name','description','effect'],
    "Weapons" : ['name','description','attack','defence', 'required_Attributes' ,'weapon_class','weight','scales_With']
}

special_fields = {
    "Ammos" : {'attack_Power'},
    "Armors" : {'damage_Negation','resistance'},
    "Weapons" : {'attack','defence', 'required_Attributes','scales_With'},
    "Bosses" : {'drops'},
    "Classes" : {'starting_stats'},
    "Creatures" : {'drops'},
    "Incantations" : {'required_Attributes'},
    "Sorceries" : {'required_Attributes'},
    "Shields" : {'attack', 'defence','required_Attributes', 'scales_With'}

}

categories = [
    'Ammos',
    'Armors',
    'Ashes',
    'Bosses',
    'Classes',
    'Creatures',
    'Incantations',
    'Locations',
    'Npcs',
    'Shields',
    'Sorceries',
    'Spirits',
    'Talismans',
    'Weapons'
]
