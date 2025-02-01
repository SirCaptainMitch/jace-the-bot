from pathlib import Path
from datetime import datetime
import typer

from jace.utils import get_config, save_config
from jace.database import get_db


app_name = 'jace'
config_name = 'config.yml'
app_dir = typer.get_app_dir(app_name=app_name, roaming=True)
conf_path: Path = Path(app_dir) / config_name
base_config_path = Path('./jace') / config_name

conf_path.parent.mkdir(parents=True, exist_ok=True)

if not conf_path.exists():
    save_config(
        path=conf_path
        , file_name=str(config_name)
        , reset=True
    )

app_config = get_config(str(conf_path))
log_path: Path = Path(app_dir) / 'jace.log'
cache_path: Path = Path(app_dir) / app_config['base_cache_dir']
data_path: Path = Path(app_dir) / app_config['base_data_dir']
db_path: Path = Path(app_dir) / app_config['database'].get('file_path')

data_path.mkdir(parents=True, exist_ok=True)
cache_path.mkdir(parents=True, exist_ok=True)

CURRENT_DATE = datetime.now().date().strftime('%Y%m%d')
FILE_POST_FIX = f'_{CURRENT_DATE}.json'

jace_db = get_db(path=str(db_path), read_only=False)


if __name__ == '__main__':
    pass
