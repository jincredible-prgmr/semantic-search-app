
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data/elden-ring-data')


"""
Config to retreive desired fields for each category
"""
field_config = {
    'Ammos' : ['name', 'description', 'type', 'attackPower', 'passive'],
    'Armors': ['name','description','category','dmgNegation','resistance','weight'],
    'Ashes' : ['name','description','affinity','skill'],
    'Bosses' : ['name','region','description','location','drops','healthPoints'],
    'Classes' : ['name','description','stats'],
    'Creatures' : ['name','description','location','drops'],
    'Incantations' : ['name','description','type','cost','slots','effects','requires'],
    'Items' : ['name','description','type','effect','obtainedFrom'],
    'Locations' : ['name','region','description'],
    'Npcs' : ['name','quote','location','role'],
    'Shields' : ['name','description','attack','defence','scalesWith','requiredAttributes','category','weight'],
    'Sorceries' : ['name','description','type','cost','slots','effects','requires'],
    'Spirits' : ['name','description','fpCost','hpCost','effect'],
    'Talismans' : ['name','description','effect'],
    "Weapons" : ['name','description','attack','defence', 'requiredAttributes' ,'category','weight']
}

special_fields = {
    "Ammos" : {'attackPower'},
    "Armors" : {'dmgNegation','resistance'},
    "Weapons" : {'attack','defence', 'requiredAttributes'},
    "Bosses" : {'drops'},
    "Classes" : {'stats'},
    "Creatures" : {'drops'},
    "Incantations" : {'requires'},
    "Sorceries" : {'requires'},
    "Shields" : {'attack', 'defence','requiredAttributes', 'scalesWith'}

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
