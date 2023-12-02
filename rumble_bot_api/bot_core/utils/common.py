from pathlib import Path
import re
import json

CURR = Path(__file__).resolve().parent
RUMBLE_BOT_API_FOLDER = CURR.parent.parent
ASSETS_FOLDER = RUMBLE_BOT_API_FOLDER / 'assets'
MINIS_FOLDER = ASSETS_FOLDER / 'minis'
TOWER_IMAGE = ASSETS_FOLDER / 'other' / 'tower.png'
ALLOWED_MINI_ARGS = ['no_skill', 'skill_1', 'skill_2', 'skill_3']


def get_all_mini_asset_names() -> list[str]:
    return [item.name.split('.')[0] for item in MINIS_FOLDER.iterdir()]


def find_root_dir() -> Path:
    current_path = CURR

    while True:
        curr = current_path / 'venv'
        if curr.exists() and current_path.is_dir():
            return current_path

        if curr.name.lower() == 'users':
            raise Exception('Could not find project root, please create a venv')

        current_path = current_path.parent
