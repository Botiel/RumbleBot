import logging
import pyautogui
from time import sleep
from rumble_bot_api.desktop_automation_tool import Processor, Position, ImagePosition
from rumble_bot_api.bot_core.mini_assets import MINI_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import Asset, Node
from rumble_bot_api.bot_core.utils.constants import TOWER_IMAGE
from rumble_bot_api.bot_core.handlers.gold_handler import GoldHandler
import rumble_bot_api.bot_core.utils.custom_exceptions as ex
from random import choice
from dataclasses import dataclass


@dataclass(kw_only=True)
class DropZone:
    LEFT: Position
    RIGHT: Position
    TOP: Position
    BOTTOM: Position


class MinisDropHandler:

    def __init__(self, processor: Processor):
        self.processor = processor
        self.gold_handler = GoldHandler(processor)

    # -------------------------------------------- CALCULATIONS --------------------------------------------------------

    def _init_tower_center_by_pixels(self, tower_ssim: float = 0.7) -> Position:
        x, y, ssim = self.processor.image_processing.find_object_on_screen_get_coordinates(image_path=str(TOWER_IMAGE))
        if ssim > tower_ssim:
            logging.info(f'[Drop Handler] Tower Center by pixels: ({x}, {y})')
            return Position(x=x, y=y)
        raise ex.ImageNotFoundException

    def _calculate_drop_zones_for_quests(self) -> DropZone:
        logging.info('[Drop Handler] Calculating Tower Center')
        tower_center = self._init_tower_center_by_pixels()

        x_offset = 120
        y_offset = -80
        center_y_offset = -120
        bottom_y_offset = 30

        x = tower_center.x
        y = tower_center.y

        return DropZone(
            LEFT=Position(x=x - x_offset, y=y + y_offset),
            RIGHT=Position(x=x + x_offset, y=y + y_offset),
            TOP=Position(x=x, y=y + center_y_offset),
            BOTTOM=Position(x=x, y=y + bottom_y_offset)
        )

    def get_current_minis_on_board(self, lineup: list[Node]) -> dict:
        results = {}
        for pick in lineup:
            x, y, ssim = self.processor.image_processing.find_object_on_screen_get_coordinates(
                image_path=pick.path,
                specific_region=MINI_ASSETS.region
            )
            if ssim > MINI_ASSETS.ssim:
                results.update({pick.name: Position(x=x, y=y)})
        return results

    # --------------------------------------------- MINIS DROP ---------------------------------------------------------


if __name__ == '__main__':
    from pathlib import Path
    from pprint import pprint

    root = Path(__file__).resolve().parent.parent.parent.parent
    yaml_file = root / 'config.yaml'
    p = Processor(yaml_file)
    p.window.set_window()
    handler = MinisDropHandler(p)
    _lineup = [
        MINI_ASSETS.baron_rivendare.skill_1,
        MINI_ASSETS.necromancer.no_skill,
        MINI_ASSETS.prowler.skill_1,
        MINI_ASSETS.ghoul.no_skill
    ]
    current = handler.get_current_minis_on_board(_lineup)
    pprint(current)
