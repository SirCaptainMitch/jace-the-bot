from pathlib import Path
from pydantic import BaseModel, Field

from src.gatherer.config import CURRENT_RULE_TXT
from src.gatherer.endpoints import RulesEndpoint
from src.gatherer.config import DEFAULT_CACHE_DIRECTORY
from rich.console import Console
console = Console()

# cache_dir: str = './.cache'


def save_file_to_directory(file_name, content, directory: str , output_type: str = 'txt'):
    # Create a Path object for the directory
    dir_path = Path(directory)

    # Ensure the directory exists
    dir_path.mkdir(parents=True, exist_ok=True)

    # Create the file path
    file_path = dir_path / file_name

    if output_type == 'txt':
        with open(file_path, 'wb') as file:
            file.write(content)


class Gatherer(BaseModel):
    cache_dir: str | None = Field(default=DEFAULT_CACHE_DIRECTORY)
    output_file_name: str | None = Field(default=f'{CURRENT_RULE_TXT}')

    def generate_rules(self, file_name: str | None = None, directory: str | None = None):
        if not file_name:
            file_name = self.output_file_name

        if not directory:
            directory = self.cache_dir
        console.print(DEFAULT_CACHE_DIRECTORY)

        rules_text = RulesEndpoint().get_txt_rules()
        save_file_to_directory(file_name=file_name, content=rules_text, directory=directory)


if __name__ == '__main__':
    pass



