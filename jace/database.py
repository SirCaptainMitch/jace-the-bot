import duckdb
import pandas as pd
from jace.utils import save_file_to_directory, save_file_to_temp_directory
from scryfall.endpoints import CatalogEndpoint, BulkEndpoint, SetEndpoint

db = duckdb.connect(database=':memory:')

cache_dir: str = '.cache'


def generate_data_cache():
    oracle_cards = BulkEndpoint().get_oracle_cards()
    save_file_to_directory(file_name='jace_oracle_cards.json', content=oracle_cards, directory=cache_dir)

    rulings = BulkEndpoint().get_rulings()
    save_file_to_directory(file_name='jace_rulings.json', content=rulings, directory=cache_dir)

    default_cards = BulkEndpoint().get_default_cards()
    save_file_to_directory(file_name='jace_default_cards.json', content=default_cards, directory=cache_dir)

    unique_artwork = BulkEndpoint().get_unique_artwork()
    save_file_to_directory(file_name='jace_unique_artwork.json', content=unique_artwork, directory=cache_dir)

    all_cards = BulkEndpoint().get_all_cards()
    save_file_to_directory(file_name='jace_all_cards.json', content=all_cards, directory=cache_dir)

    all_sets = BulkEndpoint().get_sets()
    save_file_to_directory(file_name='jace_sets.json', content=all_sets, directory=cache_dir)


def generate_oracle_cache():
    """Generates a cached file for the Scryfall oracle cards endpoint."""
    oracle_cards = BulkEndpoint().get_oracle_cards()
    save_file_to_directory(file_name='jace_oracle_cards.json', content=oracle_cards, directory=cache_dir)


def generate_card_rulings_cache():
    """Generates a cached file for the Scryfall card rulings endpoint."""
    rulings = BulkEndpoint().get_rulings()
    save_file_to_directory(file_name='jace_rulings.json', content=rulings, directory=cache_dir)


def generate_default_cards_cache():
    """Generates a cached file for the Scryfall default cards endpoint."""
    default_cards = BulkEndpoint().get_default_cards()
    save_file_to_directory(file_name='jace_default_cards.json', content=default_cards, directory=cache_dir)


def generate_unique_artwork_cache():
    """Generates a cached file for the Scryfall unique artwork cards endpoint."""
    unique_artwork = BulkEndpoint().get_unique_artwork()
    save_file_to_directory(file_name='jace_unique_artwork.json', content=unique_artwork, directory=cache_dir)


def generate_all_cards_cache():
    """Generates a cached file for the Scryfall all cards endpoint."""
    all_cards = BulkEndpoint().get_all_cards()
    save_file_to_directory(file_name='jace_all_cards.json', content=all_cards, directory=cache_dir)


def generate_sets_cache():
    """Generates a cached file for the Scryfall sets endpoint."""
    rulings = SetEndpoint().get_sets()
    save_file_to_directory(file_name='jace_sets.json', content=rulings, directory=cache_dir)


def generate_catalog_table(table: str):

    catalog_endpoint = CatalogEndpoint()
    uri_name = table
    table_name = table.replace('-', '_')
    data = catalog_endpoint.get_catalog(name=uri_name)

    df = pd.DataFrame(data=data, columns=['name'])
    db.register('data_df', df)
    db.execute(f'CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM data_df')

    return db.sql(f'SELECT * FROM {table_name}').fetchdf().count()
