import ujson as json
from pathlib import Path
from pydantic import ValidationError

from gatherer import Gatherer
from scryfall.models import *
from database import generate_data_cache

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

    refresh_cache: bool = False

    if refresh_cache:
        # generate_catalog_tables()
        generate_data_cache()

    # [print(x) for x in parse_oracle_cards()]
    Gatherer().generate_rules()

