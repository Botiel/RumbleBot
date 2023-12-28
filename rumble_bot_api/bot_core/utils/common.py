from rumble_bot_api.desktop_automation_tool.utils.data_objects import ImageElement
from pathlib import Path
import logging

CURR = Path(__file__).resolve().parent
RUMBLE_BOT_API_FOLDER = CURR.parent.parent
ASSETS_FOLDER = RUMBLE_BOT_API_FOLDER / 'assets'
MINIS_FOLDER = ASSETS_FOLDER / 'minis'
HEROES_FOLDER = ASSETS_FOLDER / 'heroes'
OTHER_FOLDER = ASSETS_FOLDER / 'other'
TOWER_IMAGE = OTHER_FOLDER / 'tower.png'
ALLOWED_MINI_ARGS = ['skill_0', 'skill_1', 'skill_2', 'skill_3']

COLLECTION_ELEMENT = ImageElement(
    name='collection_icon',
    path=str(OTHER_FOLDER / 'collection.png'),
    ssim=0.8
)

MAP_ELEMENT = ImageElement(
    name='map_icon',
    path=str(OTHER_FOLDER / 'map.png'),
    ssim=0.8
)

ACT_1_ELEMENT = ImageElement(
    name='act_1',
    path=str(OTHER_FOLDER / 'act1.png'),
    ssim=0.8
)

ACT_2_ELEMENT = ImageElement(
    name='act_2',
    path=str(OTHER_FOLDER / 'act2.png'),
    ssim=0.8
)

LEVELUP_HEART = ImageElement(
    name='levelup_heart',
    path=str(OTHER_FOLDER / 'levelup.png'),
    ssim=0.7
)


def set_logger(log_level: int = logging.DEBUG) -> None:
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_all_mini_asset_names() -> list[str]:
    return [item.name.split('.')[0] for item in MINIS_FOLDER.iterdir()]
