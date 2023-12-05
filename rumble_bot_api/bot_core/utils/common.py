from pathlib import Path
import logging

CURR = Path(__file__).resolve().parent
RUMBLE_BOT_API_FOLDER = CURR.parent.parent
ASSETS_FOLDER = RUMBLE_BOT_API_FOLDER / 'assets'
MINIS_FOLDER = ASSETS_FOLDER / 'minis'
TOWER_IMAGE = ASSETS_FOLDER / 'other' / 'tower.png'
ALLOWED_MINI_ARGS = ['no_skill', 'skill_1', 'skill_2', 'skill_3']


def set_logger(log_level: int = logging.DEBUG) -> None:
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_all_mini_asset_names() -> list[str]:
    return [item.name.split('.')[0] for item in MINIS_FOLDER.iterdir()]
