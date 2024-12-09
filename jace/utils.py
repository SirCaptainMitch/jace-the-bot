import os
import json
import typing
import tempfile
from pathlib import Path
from typing import TypeVar

from omegaconf import OmegaConf, DictConfig


DataT = TypeVar('DataT')


def get_config(path: str | Path) -> DictConfig:
    basedir = os.path.abspath(os.path.dirname(__file__))
    path = Path(os.path.join(basedir, path))
    obj = OmegaConf.load(path)
    return obj


def save_config(
        path: str | Path
        , config: dict | None = None
        , reset: bool | None = False
        , resolve: bool | None = True
        , file_name: str | None = 'config.yml'
):
    """Resolve and save the config to the app directory."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if reset:
        config = get_config(path=file_name)

    if resolve:
        OmegaConf.resolve(config)

    OmegaConf.save(config, str(path))


def useful_repr(cls: typing.Type):
    """Take the function arguments and make a string out of them dynamically"""

    def generate_repr(self):
        class_name = cls.__name__

        actual_args = ", ".join(f'{name}={getattr(self, name)!r}' for name in cls.__annotations__)

        return f"{class_name}({actual_args})"

    cls.__repr__ = generate_repr
    return cls


def save_file_to_directory(file_name: str, content: typing.Any, directory: str):
    dir_path = Path(directory)
    dir_path.mkdir(parents=True, exist_ok=True)
    file_path = dir_path / file_name
    with open(file_path, 'w') as file:
        file.write(json.dumps(content, indent=5))


def save_file_to_temp_directory(file_name: str, content: typing.Any):
    temp_dir = Path(tempfile.gettempdir())
    file_path = temp_dir / file_name
    with open(file_path, 'w') as file:
        file.write(json.dumps(content, indent=5))

    return file_path


if __name__ == '__main__':
    pass
