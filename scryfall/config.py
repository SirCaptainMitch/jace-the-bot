from datetime import datetime

BASE_URI = 'https://api.scryfall.com/'
BASE_DATA_URI = 'https://data.scryfall.io'

DEFAULT_CACHE_DIRECTORY = './.cache'
CURRENT_RULE_FMT = '%Y%m%d'
CURRENT_DATE = datetime.now().date().strftime(CURRENT_RULE_FMT)
FILE_POST_FIX = f'_{CURRENT_DATE}.json'

catalog_endpoints = [
    'card-names'
    , 'artist-names'
    , 'word-bank'
    , 'creature-types'
    , 'planeswalker-types'
    , 'land-types'
    , 'artifact-types'
    , 'enchantment-types'
    , 'spell-types'
    , 'powers'
    , 'toughnesses'
    , 'loyalties'
    , 'watermarks'
    , 'keyword-abilities'
    , 'keyword-actions'
    , 'ability-words'
]

