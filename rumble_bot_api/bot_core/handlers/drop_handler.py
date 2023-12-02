import logging
import pyautogui
from time import sleep
from rumble_bot_api.desktop_automation_tool import Processor, Position, ImagePosition
from rumble_bot_api.bot_core.utils.load_images import get_lineup_from_minis_dict, create_minis_dict
from rumble_bot_api.bot_core.utils.load_images import TOWER_IMAGE
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

    def get_current_minis_on_board(self, minis_dict: dict, lineup: list[str]) -> dict[ImagePosition]:
        element_lineup = get_lineup_from_minis_dict(minis_dict, lineup)
        results = {}
        for k, v in element_lineup.items():
            element = self.processor.image_processing.find_element(v)
            if element.ssim > v.ssim:
                results.update({k: v})
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
    _minis_dict = create_minis_dict()
    _lineup = ['baron_1', 'harpies_1', 'pilot_0', 'prowler_0', 'necromancer_0', 'ghoul_0', 'gryphon_0']
    current = handler.get_current_minis_on_board(_minis_dict, _lineup)
    pprint(current)
