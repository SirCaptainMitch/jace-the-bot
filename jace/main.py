import ujson as json
from pathlib import Path
from pydantic import ValidationError
from jace.config import CACHE_PATH
from jace.constants import cache_path
from gatherer import Gatherer
from scryfall import Scryfall, Card
from jace.database import generate_data_cache
from rich.panel import Panel
from rich import print


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


if __name__ == '__main__':
    print(Panel("Hello, [blue]World!", title="Welcome", subtitle="Thank you"))

    gatherer = Gatherer()
    scryfall = Scryfall()
    refresh_cache: bool = True

    # gatherer.generate_rules()
    if refresh_cache:
        scryfall.generate_catalogs()
        # scryfall.generate_oracle_cards()
        # scryfall.generate_rulings()

        generate_data_cache(cache_dir=str(cache_path))


    # def generate_catalog_table(table: str):
    #     data = catalog_endpoint.get_catalog(name=uri_name)
    #
    #     df = pd.DataFrame(data=data, columns=['name'])
    #     db.register('catalog', df)
    #     db.execute(f'CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM data_df')
    #
    #     return db.sql(f'SELECT * FROM {table_name}').fetchdf().count()

