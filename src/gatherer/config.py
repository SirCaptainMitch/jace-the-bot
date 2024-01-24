from datetime import datetime
from rich.console import Console

BASE_URI = 'https://media.wizards.com/2023/downloads/MagicCompRules%20'
DEFAULT_CACHE_DIRECTORY = './.cache/gatherer_rules'
CURRENT_RULE_TXT = '20231013.txt'
CURRENT_RULE_PDF = '20231013.pdf'
CURRENT_RULE_FMT = '%Y%m%d'
CURRENT_RULE_URI = f'{BASE_URI}{CURRENT_RULE_TXT}'

CURRENT_DATE_RULE_TXT = datetime.now().date().strftime(CURRENT_RULE_FMT)
CURRENT_DATE_RULE_URI = f'{BASE_URI}{CURRENT_DATE_RULE_TXT}.txt'

console = Console()
console.print(DEFAULT_CACHE_DIRECTORY)
