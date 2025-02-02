## https://api.scryfall.com/bulk-data
## The main scryfall api endpoints for bulk data.
from pathlib import Path
import ujson as json
from pydantic import BaseModel, Field
from scryfall.endpoints import CatalogEndpoint, BulkEndpoint, SetEndpoint
from scryfall.config import catalog_endpoints, FILE_POST_FIX
from scryfall.config import DEFAULT_CACHE_DIRECTORY


def save_file_to_directory(file_name, content, directory: str = DEFAULT_CACHE_DIRECTORY, output_type: str = 'txt'):
    # Create a Path object for the directory
    dir_path = Path(directory)

    # Ensure the directory exists
    dir_path.mkdir(parents=True, exist_ok=True)

    # Create the file path
    file_path = dir_path / file_name

    if output_type == 'txt':
        with open(file_path, 'wb') as file:
            file.write(content)

    if output_type == 'json':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
        # json.dump(content, file_path, indent=4, ensure_ascii=False)


def data_generator(file_name: str, directory: str, endpoint: callable):
    """Base data generator helper function."""
    res = endpoint()### Need to call the endpoint param here.
    save_file_to_directory(
        file_name=file_name, content=res, directory=directory, output_type='json'
    )


class Scryfall(BaseModel):

    cache_dir: str | None = Field(default=DEFAULT_CACHE_DIRECTORY)
    file_path_post_fix: str | None = Field(default=FILE_POST_FIX)
    bulk_endpoint: BulkEndpoint | None = Field(default_factory=BulkEndpoint)
    catalog_endpoint: CatalogEndpoint | None = Field(default_factory=CatalogEndpoint)
    set_endpoint: SetEndpoint | None = Field(default_factory=SetEndpoint)

    def generate_rulings(self, file_name: str = 'rulings', directory: str | None = None):
        directory = directory if directory else self.cache_dir
        file_name = f'{file_name}{self.file_path_post_fix}'
        data_generator(file_name=file_name, directory=directory, endpoint=self.bulk_endpoint.get_rulings)

    def generate_oracle_cards(self, file_name: str = 'oracle_cards', directory: str | None = None):
        directory = directory if directory else self.cache_dir
        file_name = f'{file_name}{self.file_path_post_fix}'
        data_generator(file_name=file_name, directory=directory, endpoint=self.bulk_endpoint.get_oracle_cards)

    def generate_catalogs(self, catalogs: list[str] | None = None, directory: str | None = None):
        directory = directory if directory else self.cache_dir
        directory = f'{directory}/catalogs'

        catalogs = catalogs if catalogs else catalog_endpoints

        for catalog in catalogs:
            file_name = f'{catalog}{self.file_path_post_fix}'
            data_generator(file_name=file_name, directory=directory, endpoint=self.catalog_endpoint.get_catalog)

    def generate_sets(self, file_name: str = 'sets', directory: str | None = None):
        """Generates sets data from the Scryfall API."""
        directory = directory if directory else self.cache_dir
        file_name = f'{file_name}{self.file_path_post_fix}'
        data_generator(file_name=file_name, directory=directory, endpoint=self.set_endpoint.get_sets)

    def generate_all_cards(self, file_name: str = 'sets', directory: str | None = None):
        """Generates all card data from the Scryfall API. This is a very large data set and could take time."""
        directory = directory if directory else self.cache_dir
        file_name = f'{file_name}{self.file_path_post_fix}'
        data_generator(file_name=file_name, directory=directory, endpoint=self.bulk_endpoint.get_all_cards)

    def generate_unique_cards(self, file_name: str = 'sets', directory: str | None = None):
        """Generates unique card data from the Scryfall API"""
        directory = directory if directory else self.cache_dir
        file_name = f'{file_name}{self.file_path_post_fix}'
        data_generator(file_name=file_name, directory=directory, endpoint=self.bulk_endpoint.get_unique_cards)

    def generate_default_cards(self, file_name: str = 'sets', directory: str | None = None):
        """Generates default cards data from the Scryfall API"""
        directory = directory if directory else self.cache_dir
        file_name = f'{file_name}{self.file_path_post_fix}'
        data_generator(file_name=file_name, directory=directory, endpoint=self.bulk_endpoint.get_default_cards())


if __name__ == '__main__':
    pass
