import os
import json
import requests


SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')
USER_RANKS_PATH = os.path.join(DATA_DIR, 'user_ranks.json')

PKMN_DIR = os.path.join(DATA_DIR, 'pokemon_data')
DEX_ID_TO_NAME_DIR = os.path.join(PKMN_DIR, 'pokemon/dexid_to_name.json')
NAME_TO_DEX_ID_DIR = os.path.join(PKMN_DIR, 'pokemon/name_to_dexid.json')
PK_DATA_PATH = os.path.join(PKMN_DIR, 'pokemon/pokemon_data.json')
ABILITY_NORMAL_PATH = os.path.join(PKMN_DIR, 'ability_normal.png')
ABILITY_HIDDEN_PATH = os.path.join(PKMN_DIR, 'ability_hidden.png')
POKEBALLHD_PATH = os.path.join(PKMN_DIR, 'pokeballhd.png')

PKMN_SPRITE_BATTLE_FRONT_NORMAL = os.path.join(PKMN_DIR, 'pokemon/battle/front/normal/')
PKMN_SPRITE_BATTLE_FRONT_SHINY = os.path.join(PKMN_DIR, 'pokemon/battle/front/shiny/')
PKMN_SPRITE_BATTLE_BACK_NORMAL = os.path.join(PKMN_DIR, 'pokemon/battle/back/normal/')
PKMN_SPRITE_BATTLE_BACK_SHINY = os.path.join(PKMN_DIR, 'pokemon/battle/back/shiny/')
PKMN_SPRITE_ARTWORK = os.path.join(PKMN_DIR, 'pokemon/artwork/ken_sugimori/')
PKMN_SPRITE_MENU = os.path.join(PKMN_DIR, 'pokemon/menu/')

PKMN_APRICORN_DIR = os.path.join(PKMN_DIR, 'icons/apricorn')
PKMN_AVCANDY_DIR = os.path.join(PKMN_DIR, 'icons/av-candy')
PKMN_BALLS_DIR = os.path.join(PKMN_DIR, 'icons/ball/')
PKMN_BATTLEITEM_DIR = os.path.join(PKMN_DIR, 'icons/battle-item')
PKMN_BERRY_DIR = os.path.join(PKMN_DIR, 'icons/berry')
PKMN_BODYSTYLE_DIR = os.path.join(PKMN_DIR, 'icons/body-style')
PKMN_CURRYINGREDIENT_DIR = os.path.join(PKMN_DIR, 'icons/curry-ingredient')
PKMN_EVITEM_DIR = os.path.join(PKMN_DIR, 'icons/ev-item')
PKMN_EVOITEM_DIR = os.path.join(PKMN_DIR, 'icons/evo-item')
PKMN_EXPCANDY_DIR = os.path.join(PKMN_DIR, 'icons/exp-candy')
PKMN_FOSSIL_DIR = os.path.join(PKMN_DIR, 'icons/fossil')
PKMN_GEM_DIR = os.path.join(PKMN_DIR, 'icons/gem')
PKMN_HOLDITEM_DIR = os.path.join(PKMN_DIR, 'icons/hold-item')
PKMN_KEYITEM_DIR = os.path.join(PKMN_DIR, 'icons/key-item')
PKMN_MEGASTONE_DIR = os.path.join(PKMN_DIR, 'icons/mega-stone')
PKMN_MEMORY_DIR = os.path.join(PKMN_DIR, 'icons/memory')
PKMN_MINT_DIR = os.path.join(PKMN_DIR, 'icons/mint')
PKMN_MULCH_DIR = os.path.join(PKMN_DIR, 'icons/mulch')
PKMN_OTHERITEM_DIR = os.path.join(PKMN_DIR, 'icons/other-item')
PKMN_PLATE_DIR = os.path.join(PKMN_DIR, 'icons/plate')
PKMN_POKECANDY_DIR = os.path.join(PKMN_DIR, 'icons/poke-candy')
PKMN_POKEMON_DIR = os.path.join(PKMN_DIR, 'icons/pokemon/')
PKMN_TYPES_DIR = os.path.join(PKMN_DIR, 'misc/types/gen8/')

PREFIX = os.getenv('PREFIX', False)
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', False)

SLICKDEALS_HOMEPAGE = 'https://slickdeals.net'
JABHAX_ICON = 'https://www.jabhax.io/static/portfolio/images/logo_transparent.png'
BOT_PROFILE_PIC = os.path.join(DATA_DIR, 'bot_profile_photo.jpeg')
PIXEL_PLAYGROUND_LOGO = os.path.join(DATA_DIR, 'pixel_playground_logo.png')
VOWELS = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
WORDS_DICTIONARY = os.path.join(DATA_DIR, 'words_dictionary.json')

REDDIT_APP_ID = os.getenv('REDDIT_APP_ID', False)
REDDIT_APP_SECRET = os.getenv('REDDIT_APP_SECRET', False)
REDDIT_ENABLED_MEME_SUBREDDITS = ['funny', 'memes']
REDDIT_ENABLED_NSFW_SUBREDDITS = ['wtf']

DEBUG_LOGS = bool(eval(os.getenv('DEBUG_LOGS')))

def write_resource(path, data, write_ops='w'):
    with open(os.path.join(path), write_ops) as f:
        f.write(json.dumps(data))

def load_resource(path):
    resource = {}
    with open(os.path.join(path), 'r') as f:
        resource = json.load(f)
    return resource
try:
    PK_JSON = load_resource(PK_DATA_PATH)
except:
    data = {}
    write_resource(PK_DATA_PATH, data)
    PK_JSON = load_resource(PK_DATA_PATH)
# PK_JSON = load_resource('/Users/justinbarros/Desktop/pokemon_data.json')
DEX_ID_TO_NAME_JSON = load_resource(DEX_ID_TO_NAME_DIR)
NAME_TO_DEX_ID_JSON = load_resource(NAME_TO_DEX_ID_DIR)
# USER_RANKS_JSON = load_resource(USER_RANKS_PATH)
