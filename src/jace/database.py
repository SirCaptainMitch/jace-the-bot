import json
from pathlib import Path
import tempfile
import duckdb
import pandas as pd
from src.scryfall.config import catalog_endpoints
from src.scryfall.endpoints import CatalogEndpoint, BulkEndpoint
from src.jace.config import progress


db = duckdb.connect(database=':memory:')

cache_dir: str = '.cache'


def save_file_to_directory(file_name, content, directory: str = cache_dir):
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / file_name
    with open(file_path, 'w') as file:
        file.write(json.dumps(content, indent=5))


def save_file_to_temp_directory(file_name, content):
    temp_dir = Path(tempfile.gettempdir())
    file_path = temp_dir / file_name
    with open(file_path, 'w') as file:
        file.write(json.dumps(content, indent=5))

    return file_path


def generate_data_cache():
    oracle_cards = BulkEndpoint().get_oracle_cards()
    # save_file_to_temp_directory(file_name='jace_oracle_cards.json', content=oracle_cards)
    save_file_to_directory(file_name='jace_oracle_cards.json', content=oracle_cards)

    rulings = BulkEndpoint().get_rulings()
    save_file_to_directory(file_name='jace_rulings.json', content=rulings)

    default_cards = BulkEndpoint().get_default_cards()
    save_file_to_directory(file_name='jace_default_cards.json', content=default_cards)

    unique_artwork = BulkEndpoint().get_unique_artwork()
    save_file_to_directory(file_name='jace_unique_artwork.json', content=unique_artwork)

    all_cards = BulkEndpoint().get_all_cards()
    save_file_to_directory(file_name='jace_all_cards.json', content=all_cards)


def generate_catalog_table(table: str):

    catalog_endpoint = CatalogEndpoint()
    uri_name = table
    table_name = table.replace('-', '_')
    data = catalog_endpoint.get_catalog(name=uri_name)

    df = pd.DataFrame(data=data, columns=['name'])
    db.register('data_df', df)
    db.execute(f'CREATE TABLE {table_name} AS SELECT * FROM data_df')

<<<<<<< HEAD:src/jace/database.py
    return db.sql(f'SELECT * FROM {table_name}').fetchdf().count()
=======
        # print(db.sql(f'SELECT * FROM {table_name}').fetchdf())
>>>>>>> b52cd4bf0f3796cad8ec8273777ab972061d773a:database.py
