from pathlib import Path
from datetime import datetime
import typer

from .utils import get_config, save_config


app_name = 'jace'
config_name = 'config.yml'
app_dir = typer.get_app_dir('jace', roaming=True)
conf_path: Path = Path(app_dir) / app_name / config_name
base_config_path = Path('./scryfall') / config_name
log_path: Path = Path(app_dir) / app_name / 'jace.log'

(Path(app_dir) / 'data').mkdir(parents=True, exist_ok=True)
(Path(app_dir) / '.cache').mkdir(parents=True, exist_ok=True)
conf_path.parent.mkdir(parents=True, exist_ok=True)

if not conf_path.exists():
    save_config(
        path=conf_path
        , file_name=str(config_name)
        , reset=True
    )

app_config = get_config(str(conf_path))

CURRENT_DATE = datetime.now().date().strftime('%Y%m%d')
FILE_POST_FIX = f'_{CURRENT_DATE}.json'


if __name__ == '__main__':
    pass

