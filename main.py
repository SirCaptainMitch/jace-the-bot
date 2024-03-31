import ujson as json
from pathlib import Path
from pydantic import ValidationError

from src.gatherer import Gatherer
from src.scryfall.models import *
# from src.database import generate_data_cache, generate_catalog_tables
from src.scryfall import Scryfall
from rich.console import Console
console = Console()

cache_dir: str = './.cache'


def parse_oracle_cards(directory: str = cache_dir, file_name: str = 'jace_default_cards.json'):
    dir_path = Path(directory)
    file_path = dir_path / file_name
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for x in data[:]:
        try:
            card = Card(**x)
            yield card
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Error parsing JSON: {e}")
            yield None
    print(len(data))


if __name__ == '__main__':
    gatherer = Gatherer()
    scryfall = Scryfall()
    refresh_cache: bool = True

    if refresh_cache:
    #     generate_catalog_tables()
    #     generate_data_cache()
        gatherer.generate_rules()
        # scryfall.generate_catalogs()
        # scryfall.generate_oracle_cards()
        # scryfall.generate_rulings()

    # [print(x) for x in parse_oracle_cards()]


