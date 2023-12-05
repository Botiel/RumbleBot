from rumble_bot_api.desktop_automation_tool.utils.data_objects import ImageElement
from pathlib import Path
import logging

CURR = Path(__file__).resolve().parent
RUMBLE_BOT_API_FOLDER = CURR.parent.parent
ASSETS_FOLDER = RUMBLE_BOT_API_FOLDER / 'assets'
MINIS_FOLDER = ASSETS_FOLDER / 'minis'
HEROES_FOLDER = ASSETS_FOLDER / 'heroes'
TOWER_IMAGE = ASSETS_FOLDER / 'other' / 'tower.png'
MAP_ICON_IMAGE = ASSETS_FOLDER / 'other' / 'map.png'
COLLECTION_ICON_IMAGE = ASSETS_FOLDER / 'other' / 'collection.png'
ALLOWED_MINI_ARGS = ['no_skill', 'skill_1', 'skill_2', 'skill_3']

COLLECTION_ELEMENT = ImageElement(
    name='collection_icon',
    path=str(COLLECTION_ICON_IMAGE),
    ssim=0.8
)

MAP_ELEMENT = ImageElement(
    name='map_icon',
    path=str(MAP_ICON_IMAGE),
    ssim=0.8
)


def set_logger(log_level: int = logging.DEBUG) -> None:
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_all_mini_asset_names() -> list[str]:
    return [item.name.split('.')[0] for item in MINIS_FOLDER.iterdir()]
