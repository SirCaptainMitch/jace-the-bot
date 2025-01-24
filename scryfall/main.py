## https://api.scryfall.com/bulk-data
## The main scryfall api endpoints for bulk data.
from pathlib import Path
import ujson as json
from pydantic import BaseModel, Field
from scryfall.endpoints import CatalogEndpoint, BulkEndpoint
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


class Scryfall(BaseModel):

    cache_dir: str | None = Field(default=DEFAULT_CACHE_DIRECTORY)

    def generate_rulings(self, file_name: str = 'rulings', directory: str | None = None):
        if not directory:
            directory = self.cache_dir

        res = BulkEndpoint().get_rulings()
        file_name = f'{file_name}{FILE_POST_FIX}'
        save_file_to_directory(
            file_name=file_name, content=res, directory=directory, output_type='json'
        )

    def generate_oracle_cards(self, file_name: str = 'oracle_cards', directory: str | None = None):
        if not directory:
            directory = self.cache_dir

        res = BulkEndpoint().get_oracle_cards()
        file_name = f'{file_name}{FILE_POST_FIX}'
        save_file_to_directory(
            file_name=file_name, content=res, directory=directory, output_type='json'
        )

    def generate_catalogs(self, catalogs: list[str] | None = None, directory: str | None = None):
        if not directory:
            directory = self.cache_dir

        if not catalogs:
            catalogs = catalog_endpoints

        directory = f'{directory}/catalogs'
        print(directory)
        for catalog in catalogs:
            res = CatalogEndpoint().get_catalog(name=catalog)
            catalog = catalog.replace('-', '_')
            file_name = f'{catalog}{FILE_POST_FIX}'
            save_file_to_directory(
                file_name=file_name, content=res, directory=directory, output_type='json'
            )


if __name__ == '__main__':
    pass



