import logging
import sys
from random import choice
from typing import Optional, Literal
from dataclasses import dataclass
from rumble_bot_api.desktop_automation_tool import Processor, Position
from rumble_bot_api.bot_core.mini_assets import MINI_ASSETS
from rumble_bot_api.bot_core.utils.common import TOWER_IMAGE
from rumble_bot_api.bot_core.utils.data_objects import Node
from rumble_bot_api.bot_core.handlers.gold_handler import GoldHandler
from rumble_bot_api.desktop_automation_tool.utils.custom_exceptions import ImageNotFoundException


@dataclass(kw_only=True)
class DropZone:
    LEFT: Position
    RIGHT: Position
    TOP: Position
    BOTTOM: Position


class DropHandler:

    def __init__(self, processor: Processor):
        self.processor = processor
        self.gold_handler = GoldHandler(processor)

        # Settings
        self.tower_center: Optional[Position] = None
        self.drop_zones: Optional[DropZone] = None
        self.game_mode: Optional[str] = None
        self.quests_lineup: Optional[list[Node]] = None
        self.pvp_lineup: Optional[list[Node]] = None

    # --------------------- SETTERS ---------------------------
    def set_quests_lineup(self, lineup: list[Node]) -> None:
        logging.info('[Drop Handler] setting up quests lineup')
        self.quests_lineup = lineup
        self.quests_lineup.append(MINI_ASSETS.miner.no_skill)

    def set_pvp_lineup(self, lineup: list[Node]) -> None:
        logging.info('[Drop Handler] setting up pvp lineup')
        self.pvp_lineup = lineup
        self.pvp_lineup.append(MINI_ASSETS.miner.no_skill)

    def set_game_mode(self, game_mode: Literal['pvp', 'quests']) -> None:

        if game_mode not in ['pvp', 'quests']:
            raise ValueError(f'No such game mode: {game_mode}')

        logging.info(f'[Drop Handler] setting up game mode: {game_mode}')
        self.game_mode = game_mode

    # ------------------- CALCULATIONS ------------------------

    def init_tower_center_by_pixels(self, tower_ssim: float = 0.6) -> None:
        x, y, ssim = self.processor.image_processing.find_object_on_screen_get_coordinates(image_path=str(TOWER_IMAGE))
        if ssim > tower_ssim:
            logging.info(f'[Drop Handler] Tower Center by pixels: ({x}, {y})')
            self.tower_center = Position(x=x, y=y)
        else:
            raise ImageNotFoundException

    def calculate_drop_zones_for_quests(self) -> None:
        logging.info('[Drop Handler] Calculating Tower Center')
        self.init_tower_center_by_pixels()

        x_offset = 120
        y_offset = -80
        center_y_offset = -120
        bottom_y_offset = 30

        x = self.tower_center.x
        y = self.tower_center.y

        self.drop_zones = DropZone(
            LEFT=Position(x=x - x_offset, y=y + y_offset),
            RIGHT=Position(x=x + x_offset, y=y + y_offset),
            TOP=Position(x=x, y=y + center_y_offset),
            BOTTOM=Position(x=x, y=y + bottom_y_offset)
        )

    def get_current_minis_on_board(self) -> dict:
        results = {}
        lineup = None

        if not self.game_mode:
            logging.error('[Drop Handler] game mode is not set!')
            sys.exit(1)

        if self.game_mode == 'pvp':
            lineup = self.pvp_lineup

        if self.game_mode == 'quests':
            lineup = self.quests_lineup

        if not lineup:
            logging.error('[Drop Handler] lineups are not set!')
            sys.exit(1)

        for mini in lineup:
            x, y, ssim = self.processor.image_processing.find_object_on_screen_get_coordinates(
                image_path=mini.path,
                specific_region=MINI_ASSETS.region
            )
            if ssim > MINI_ASSETS.ssim:
                results.update({mini.name: [Position(x=x, y=y), mini.cost]})
        return results

    # -------------------- MINIS DROP --------------------------

    def drop_mini(self, mini: str, dropzone: Position) -> bool:

        current_minis = self.get_current_minis_on_board()
        result = current_minis.get(mini)

        if not result:
            logging.info(f'[Drop Handler] Did not find mini on board: {mini}')
            return False

        mini_position, cost = result

        self.gold_handler.wait_until_enough_gold(cost)
        before_gold_count = self.gold_handler.get_current_gold_on_bar()
        self.processor.actions.drag_and_drop(mini_position, dropzone, wait_after_drop=0.5)
        after_gold_count = self.gold_handler.get_current_gold_on_bar()

        return before_gold_count > after_gold_count

    def drop_miner_for_quests(self) -> bool:

        # Finding miner position on screen
        miner_x, miner_y, miner_ssim = self.processor.image_processing.find_object_on_screen_get_coordinates(
            image_path=MINI_ASSETS.miner.no_skill.path,
            specific_region=MINI_ASSETS.region
        )

        miner_pos = Position(x=miner_x, y=miner_y)

        if miner_ssim < MINI_ASSETS.ssim:
            logging.info('[Drop Handler] Did not find miner on the board')
            return False

        # Finding gold ore positions
        gold_positions = self.gold_handler.check_for_gold_ore_get_positions()
        if not gold_positions:
            logging.info('[Drop Handler] Did not find gold ore')
            return False

        if self.game_mode is None:
            logging.error('[Drop Handler] game mode is not set!')
            sys.exit(1)
        else:
            gold_pos = choice(gold_positions)
            if gold_pos.x > self.tower_center.x:
                zone = self.drop_zones.RIGHT
            else:
                zone = self.drop_zones.LEFT

        self.gold_handler.wait_until_enough_gold(1)
        before_gold_count = self.gold_handler.get_current_gold_on_bar()
        self.processor.actions.drag_and_drop(miner_pos, zone, wait_after_drop=0.5)
        after_gold_count = self.gold_handler.get_current_gold_on_bar()

        return before_gold_count > after_gold_count
