import logging
from time import sleep, time

import pyautogui

from rumble_bot_api.desktop_automation_tool.processors_loader import Processor
from rumble_bot_api.bot_core.string_assets import STRING_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import GameState
from rumble_bot_api.bot_core.handlers.base_handler import BaseHandler
from rumble_bot_api.bot_core.utils.custom_exceptions import NoMinisOnBoardException, GoldNotFoundException
from rumble_bot_api.bot_core.utils.data_objects import PvpMatchObject
from rumble_bot_api.bot_core.handlers.drop_handler import DropHandler
from rumble_bot_api.bot_core.mini_assets import MINI_ASSETS
from typing import Optional


class PvpHandler(BaseHandler):

    def __init__(self, processor: Processor):
        super().__init__(processor)
        self.set_game_mode('pvp')
        self.match_object: Optional[PvpMatchObject] = None

    def set_pvp_match_object(self, match_object: PvpMatchObject) -> None:
        logging.info('[PvP Handler] setting up PVP match object and drop handler')
        logging.debug(f'[PvP Handler] lineup: {match_object.lineup}')
        self.match_object = match_object
        lineup = match_object.lineup
        lineup.append(MINI_ASSETS.miner.skill_0)
        self.drop_handler = DropHandler(self._processor, lineup)

    def init_pvp(self) -> None:
        logging.info('[PvP Handler] Initializing PVP match')

        if self.actions.wait_and_try_click_string_element(STRING_ASSETS.CLAIM, 4, ignore_exception=True):
            self.handle_level_up()

        self.actions.wait_and_try_click_string_element(STRING_ASSETS.PVP, ignore_exception=True)
        self.actions.wait_and_try_click_string_element(STRING_ASSETS.RUMBLE_PVP)

        self.wait_for_load_state(60)

        self.set_game_state(GameState.PVP_MATCH_LOOP)

    def match_loop(self) -> None:
        logging.info('[PvP Handler] Starting a PvP Match')

        self.tesseract.wait_for_element_state(STRING_ASSETS.VS, state='visible')

        self.match_object.scroll_up_before_match()

        method, item = self.match_object.click_arrows_before_match()

        self.wait_for_match_to_start()

        if method and item:
            method(item)

        while True:
            try:
                self.match_object.drop_logic()
            except (GoldNotFoundException, NoMinisOnBoardException):
                self.set_game_state(GameState.PVP_GAME_FINISH)
                return

            error = [
                self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.ERROR),
                self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.FAILED),
                self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.TOOLS)
            ]
            if any(error):
                self.set_game_state(GameState.ERROR_STATE)
                return

    def match_finish(self) -> None:

        logging.info('[PvP Handler] game finished')

        is_continue = None
        start_time = time()
        while time() - start_time < 15:
            is_continue = self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.CONTINUE)
            if is_continue:
                break
            sleep(0.5)

        if not is_continue:
            self.set_game_state(GameState.ERROR_STATE)
            return

        if is_continue:
            self.actions.click_string_element_until_hidden(STRING_ASSETS.CONTINUE)
            self.wait_for_load_state(60)
            self.set_game_state(GameState.INIT_PVP)
            return

    def main_loop(self) -> None:

        self.set_game_state(GameState.INIT_PVP)

        while True:
            try:
                match self._current_state:
                    case GameState.INIT_PVP:
                        self.init_pvp()
                    case GameState.PVP_MATCH_LOOP:
                        self.match_loop()
                    case GameState.PVP_GAME_FINISH:
                        self.match_finish()
                    case GameState.ERROR_STATE:
                        self.handler_errors()
            except Exception as e:
                logging.error(f'Something went wrong: {e}')
                self.set_game_state(GameState.ERROR_STATE)
