import duckdb as duck

from jace.constants import FILE_POST_FIX
from scryfall import Scryfall


def get_db(path: str, read_only: bool = False ) -> duck.DuckDBPyConnection:
    """Gets a connection to the duckdb database."""
    con = duck.connect(database=path, read_only=read_only)
    return con


def generate_data_cache(cache_dir: str):
    """Extracts the data from the Scryfall API and saves it to the cache directory to be consumed.
        The Scryfall API documentation requests that you limit the number of pulls to 100 per second, and while this
        would technically fit in that window for an ASYNC job, I am leaving it as synchronous out of respect for that
        request.
    """
    # TODO: Look at adding gzip or another type of compression to help reduce the file size.
    scryfall = Scryfall(cache_dir=cache_dir)
    scryfall.generate_oracle_cards(file_name=f'jace_oracle_cards')
    scryfall.generate_rulings(file_name=f'jace_rulings')
    scryfall.generate_default_cards(file_name=f'jace_default_cards')
    scryfall.generate_unique_cards(file_name=f'jace_unique_artwork')
    scryfall.generate_all_cards(file_name=f'jace_all_cards')
    scryfall.generate_sets(file_name=f'jace_sets')
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