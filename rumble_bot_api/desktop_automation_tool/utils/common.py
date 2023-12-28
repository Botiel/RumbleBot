from pathlib import Path
import os

CURR = Path(__file__).resolve().parent
ROOT = CURR.parent.parent
ASSETS_FOLDER = ROOT / 'assets'


def get_images_as_dict() -> dict:
    return {str(item.name): str(item) for item in ASSETS_FOLDER.glob('**/*') if item.is_file() and item.match('*.png')}


def find_root_dir() -> Path:
    current_path = CURR

    while True:
        curr = current_path / 'venv'
        curr2 = current_path / '.venv'

        conditions = [
            curr.exists() and current_path.is_dir(),
            curr2.exists() and current_path.is_dir()
        ]

        if any(conditions):
            return current_path

        if curr.name.lower() == 'users':
            raise Exception('Could not find project root, please create a venv')

        current_path = current_path.parent


def get_output_folder() -> Path:
    root = find_root_dir()
    folder = root / 'output'
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    return folder
