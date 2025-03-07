from datetime import datetime
from rich.console import Console

BASE_URI = 'https://media.wizards.com/2024/downloads/MagicCompRules%20'
DEFAULT_CACHE_DIRECTORY = './.cache/gatherer_rules'
CURRENT_RULE_TXT = '20241108.txt'
CURRENT_RULE_PDF = '20241108.pdf'
CURRENT_RULE_FMT = '%Y%m%d'
CURRENT_RULE_URI = f'{BASE_URI}{CURRENT_RULE_TXT}'

CURRENT_DATE_RULE_TXT = datetime.now().date().strftime(CURRENT_RULE_FMT)
CURRENT_DATE_RULE_URI = f'{BASE_URI}{CURRENT_DATE_RULE_TXT}.txt'

console = Console()
console.print(DEFAULT_CACHE_DIRECTORY)
