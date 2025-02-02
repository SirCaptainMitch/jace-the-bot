import duckdb as duck
from scryfall import Scryfall


def get_db(path: str, read_only: bool = False ) -> duck.DuckDBPyConnection:
    """Gets a connection to the duckdb database."""
    con = duck.connect(database=path, read_only=read_only)
    return con


def generate_data_cache(cache_dir: str):
    scryfall = Scryfall(cache_dir=cache_dir)
    scryfall.generate_oracle_cards(file_name='jace_oracle_cards.json')
    scryfall.generate_rulings(file_name='jace_rulings.json')
    scryfall.generate_default_cards(file_name='jace_default_cards.json')
    scryfall.generate_unique_cards(file_name='jace_unique_artwork.json')
    scryfall.generate_all_cards(file_name='jace_all_cards.json')
    scryfall.generate_sets(file_name='jace_sets.json')
    scryfall.generate_catalogs()


# def generate_cards_table(table: str):
#
#     catalog_endpoint = CatalogEndpoint()
#     uri_name = table
#     table_name = table.replace('-', '_')
#     data = catalog_endpoint.get_catalog(name=uri_name)
#
#     df = pd.DataFrame(data=data, columns=['name'])
#     db.register('data_df', df)
#     db.execute(f'CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM data_df')
#
#     return db.sql(f'SELECT * FROM {table_name}').fetchdf().count()