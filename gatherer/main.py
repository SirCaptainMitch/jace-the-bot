from pathlib import Path
from pydantic import BaseModel, Field

from gatherer.config import CURRENT_RULE_TXT
from gatherer.endpoints import RulesEndpoint


cache_dir: str = './.cache'


def save_file_to_directory(file_name, content, directory: str = cache_dir, output_type: str = 'txt'):
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
    output_directory: str | None = Field(default=cache_dir)
    output_file_name: str | None = Field(default=f'{CURRENT_RULE_TXT}')

    @staticmethod
    def generate_rules(file_name: str = CURRENT_RULE_TXT, directory: str = cache_dir):
        rules_text = RulesEndpoint().get_txt_rules()
        save_file_to_directory(file_name=file_name, content=rules_text, directory=directory)


if __name__ == '__main__':
    pass
    # output_directory = cache_dir
    # output_file_name = f'{CURRENT_RULE_TXT}'
    #
    # generate_rules(file_name=output_file_name, directory=output_directory)


