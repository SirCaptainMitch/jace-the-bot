import time
import random
import os
import sys
import ujson as json
from pathlib import Path
from pydantic import ValidationError
from src.jace.config import console, CACHE_PATH, progress
from src.gatherer import Gatherer
from src.scryfall.models import *
from src.scryfall.config import catalog_endpoints
from src.scryfall import Scryfall
from rich.panel import Panel


def parse_oracle_cards(directory: str = CACHE_PATH, file_name: str = 'jace_default_cards.json'):
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
    print(Panel("Hello, [blue]World!", title="Welcome", subtitle="Thank you"))

    gatherer = Gatherer()
    scryfall = Scryfall()
    refresh_cache: bool = True

    if refresh_cache:
        if sys.argv[1:]:
            generate_catalogs(sys.argv[1:])
        else:
            generate_catalogs(catalog_endpoints)

        # generate_catalog_tables()
        # generate_data_cache()
        # print(console)
        # gatherer.generate_rules()
        # scryfall.generate_catalogs()
        # scryfall.generate_oracle_cards()
        # scryfall.generate_rulings()

    # console.print([x for x in parse_oracle_cards()])


