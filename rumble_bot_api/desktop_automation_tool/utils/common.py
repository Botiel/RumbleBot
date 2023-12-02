from pathlib import Path
import logging
import yaml
import os

ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_FOLDER = ROOT / 'assets'


def load_yaml_file(path: str | Path) -> dict:
    logging.info('[System] Loading config.yaml file')

    if isinstance(path, str):
        path = Path(path)

    if not path.exists() and not path.is_file():
        raise FileNotFoundError('Could not find config.yaml file')

    with open(path, 'r') as file:
        data = yaml.safe_load(file)

    for k, v in data.items():
        if v is None:
            raise ValueError(f'data is missing on config.yaml file value: {k}')

    return data


def get_folder(yaml_config: dict, folder: str) -> Path:
    root = Path(yaml_config.get('project_root'))
    folder = root / folder
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    return folder


def get_images_as_dict() -> dict:
    return {str(item.name): str(item) for item in ASSETS_FOLDER.glob('**/*') if item.is_file() and item.match('*.png')}
