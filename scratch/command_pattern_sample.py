from __future__ import annotations

from abc import ABC, abstractmethod
from functools import partial
from pathlib import Path
import ujson as json
from pydantic import BaseModel, Field

from scryfall.endpoints import CatalogEndpoint, BulkEndpoint, SetEndpoint
from scryfall.config import catalog_endpoints, FILE_POST_FIX, DEFAULT_CACHE_DIRECTORY


def save_file_to_directory(
    file_name: str,
    content,
    directory: str = DEFAULT_CACHE_DIRECTORY,
    output_type: str = 'txt'
):
    """Save content to a file in the given directory."""
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / file_name

    if output_type == 'txt':
        with open(file_path, 'wb') as file:
            file.write(content)
    elif output_type == 'json':
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)


# Command interface
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        """Execute the command."""


# Concrete Command class for generating data from an endpoint.
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

    def execute(self) -> None:
        data = self.endpoint()  # Call the provided endpoint callable.
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
        return f'{base_name}{self.file_path_post_fix}'

    def _resolve_directory(self, directory: str | None) -> str:
        return directory if directory else self.cache_dir

    def execute_command(self, command: Command) -> None:
        """Execute a command."""
        command.execute()

    def generate_rulings(self, file_name: str = 'rulings', directory: str | None = None):
        directory = self._resolve_directory(directory)
        full_file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=full_file_name,
            directory=directory,
            endpoint=self.bulk_endpoint.get_rulings
        )
        self.execute_command(cmd)

    def generate_oracle_cards(self, file_name: str = 'oracle_cards', directory: str | None = None):
        directory = self._resolve_directory(directory)
        full_file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=full_file_name,
            directory=directory,
            endpoint=self.bulk_endpoint.get_oracle_cards
        )
        self.execute_command(cmd)

    def generate_catalogs(self, catalogs: list[str] | None = None, directory: str | None = None):
        directory = self._resolve_directory(directory)
        catalog_directory = f'{directory}/catalogs'
        catalogs = catalogs if catalogs else catalog_endpoints

        for catalog in catalogs:
            full_file_name = self._build_file_name(catalog.replace('-', '_'))
            # Using functools.partial to bind the catalog name to the endpoint.
            endpoint_callable = partial(self.catalog_endpoint.get_catalog, name=catalog)
            cmd = DataCommand(
                file_name=full_file_name,
                directory=catalog_directory,
                endpoint=endpoint_callable
            )
            self.execute_command(cmd)

    def generate_sets(self, file_name: str = 'sets', directory: str | None = None):
        directory = self._resolve_directory(directory)
        full_file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=full_file_name,
            directory=directory,
            endpoint=self.set_endpoint.get_sets
        )
        self.execute_command(cmd)

    def generate_all_cards(self, file_name: str = 'all_cards', directory: str | None = None):
        directory = self._resolve_directory(directory)
        full_file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=full_file_name,
            directory=directory,
            endpoint=self.bulk_endpoint.get_all_cards
        )
        self.execute_command(cmd)

    def generate_unique_cards(self, file_name: str = 'unique_cards', directory: str | None = None):
        directory = self._resolve_directory(directory)
        full_file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=full_file_name,
            directory=directory,
            endpoint=self.bulk_endpoint.get_unique_cards
        )
        self.execute_command(cmd)

    def generate_default_cards(self, file_name: str = 'default_cards', directory: str | None = None):
        directory = self._resolve_directory(directory)
        full_file_name = self._build_file_name(file_name)
        cmd = DataCommand(
            file_name=full_file_name,
            directory=directory,
            endpoint=self.bulk_endpoint.get_default_cards
        )
        self.execute_command(cmd)


if __name__ == '__main__':
    # Example usage:
    scryfall = Scryfall()
    scryfall.generate_all_cards()
