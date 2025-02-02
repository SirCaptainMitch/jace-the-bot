## https://api.scryfall.com/bulk-data
## The main scryfall api endpoints for bulk data.
from __future__ import annotations

from pathlib import Path
from functools import partial
from abc import ABC, abstractmethod

import ujson as json
from pydantic import BaseModel, Field

from scryfall.endpoints import CatalogEndpoint, BulkEndpoint, SetEndpoint
from scryfall.config import catalog_endpoints, FILE_POST_FIX, DEFAULT_CACHE_DIRECTORY


def save_file_to_directory(
        file_name: str
        , content
        , directory: str = DEFAULT_CACHE_DIRECTORY
        , output_type: str = 'txt'
):
    """Saves a text or JSON file to a directory."""
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / file_name

    if output_type == 'txt':
        with open(file_path, 'wb') as file:
            file.write(content)

    if output_type == 'json':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)


class Command(ABC):

    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""


class DataCommand(Command):
    def __init__(
        self,
        file_name: str,
        directory: str,
        endpoint: callable,
        output_type: str = 'json'
    ):
        self.file_name = file_name
        self.directory = directory
        self.endpoint = endpoint
        self.output_type = output_type

    def execute(self):
        data = self.endpoint()
        save_file_to_directory(
            file_name=self.file_name,
            content=data,
            directory=self.directory,
            output_type=self.output_type
        )


class Scryfall(BaseModel):

    cache_dir: str | None = Field(default=DEFAULT_CACHE_DIRECTORY)
    file_path_post_fix: str | None = Field(default=FILE_POST_FIX)
    bulk_endpoint: BulkEndpoint | None = Field(default_factory=BulkEndpoint)
    catalog_endpoint: CatalogEndpoint | None = Field(default_factory=CatalogEndpoint)
    set_endpoint: SetEndpoint | None = Field(default_factory=SetEndpoint)

    def _build_file_name(self, base_name: str) -> str:
        """Creates the file name with the postfix for the data."""
        return f'{base_name}{self.file_path_post_fix}'

    def _resolve_directory(self, directory: str | None = None) -> str:
        """Ensures the directory resolves to either the passed parameter or the default cache directory."""
        return directory or self.cache_dir

    @staticmethod
    def execute_command(command: Command):
        """Executes the specified command."""
        command.execute()

    def generate_rulings(self, file_name: str = 'rulings', directory: str | None = None):
        """Generates the card rulings data from the Scryfall API."""
        directory = self._resolve_directory(directory)
        file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=file_name,
            directory=directory,
            endpoint=self.bulk_endpoint.get_rulings()
        )
        self.execute_command(cmd)

    def generate_oracle_cards(self, file_name: str = 'oracle_cards', directory: str | None = None):
        """Generates the oracle cards data from the Scryfall API."""
        directory = self._resolve_directory(directory)
        file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=file_name,
            directory=directory,
            endpoint=self.bulk_endpoint.get_oracle_cards()
        )
        self.execute_command(cmd)

    def generate_catalogs(self, catalogs: list[str] | None = None, directory: str | None = None):
        """Generates catalog data for each catalog passed."""
        directory = self._resolve_directory(directory)
        directory = f'{directory}/catalogs'
        catalogs = catalogs if catalogs else catalog_endpoints

        for catalog in catalogs:
            full_file_name = self._build_file_name(catalog.replace('-', '_'))
            endpoint_callable = partial(self.catalog_endpoint.get_catalog, name=catalog)
            cmd = DataCommand(
                file_name=full_file_name,
                directory=directory,
                endpoint=endpoint_callable
            )
            self.execute_command(cmd)

    def generate_sets(self, file_name: str = 'sets', directory: str | None = None):
        """Generates sets data from the Scryfall API."""
        directory = self._resolve_directory(directory)
        file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=file_name,
            directory=directory,
            endpoint=self.set_endpoint.get_sets()
        )
        self.execute_command(cmd)

    def generate_all_cards(self, file_name: str = 'sets', directory: str | None = None):
        """Generates all card data from the Scryfall API. This is a very large data set and could take time."""
        directory = self._resolve_directory(directory)
        file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=file_name,
            directory=directory,
            endpoint=self.bulk_endpoint.get_all_cards()
        )
        self.execute_command(cmd)

    def generate_unique_cards(self, file_name: str = 'sets', directory: str | None = None):
        """Generates unique card data from the Scryfall API."""
        directory = self._resolve_directory(directory)
        file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=file_name,
            directory=directory,
            endpoint=self.bulk_endpoint.get_unique_artwork()
        )
        self.execute_command(cmd)

    def generate_default_cards(self, file_name: str = 'sets', directory: str | None = None):
        """Generates default cards data from the Scryfall API."""
        directory = self._resolve_directory(directory)
        file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=file_name,
            directory=directory,
            endpoint=self.bulk_endpoint.get_default_cards()
        )
        self.execute_command(cmd)


if __name__ == '__main__':
    # Example usage:
    scryfall = Scryfall()
    scryfall.generate_catalogs()
