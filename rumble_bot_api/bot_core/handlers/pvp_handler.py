import logging
from time import sleep, time
from typing import Callable
from rumble_bot_api.desktop_automation_tool.processors_loader import Processor
from rumble_bot_api.bot_core.string_assets import STRING_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import GameState
from rumble_bot_api.bot_core.handlers.base_handler import BaseHandler
from rumble_bot_api.bot_core.handlers.error_handler import ErrorHandler
from rumble_bot_api.desktop_automation_tool.utils.custom_exceptions import ElementNotFoundException
from rumble_bot_api.bot_core.utils.data_objects import Node


class PvpHandler(BaseHandler):

    def __init__(self, processor: Processor, lineup: list[Node], pvp_logic: Callable):
        super().__init__(processor)

        self.error_handler = ErrorHandler(processor, 'quests')
        self.lineup = lineup

        self.drop_handler.set_game_mode('pvp')
        self.drop_handler.set_pvp_lineup(lineup)
        self.pvp_logic = pvp_logic

    def init_pvp(self) -> None:
        logging.info('[PvP Handler] Initializing PVP match')

        if self.actions.wait_and_try_click_string_element(STRING_ASSETS.CLAIM, 4, ignore_exception=True):
            self.handle_level_up()

        self.actions.wait_and_try_click_string_element(STRING_ASSETS.PVP, ignore_exception=True)
        self.actions.wait_and_try_click_string_element(STRING_ASSETS.RUMBLE_PVP)

        self.wait_for_load_state(60)

        self.tesseract.wait_for_element_state(STRING_ASSETS.VS, state='visible', return_bool=True)

        self.wait_for_match_to_start()

        self.set_game_state(GameState.PVP_MATCH_LOOP)

    def match_loop(self) -> None:
        logging.info('[PvP Handler] Starting a PvP Match')

        while True:

            try:
                self.pvp_logic()
            except ElementNotFoundException:
                self.set_game_state(GameState.PVP_GAME_FINISH)
                return

            error = [
                self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.ERROR),
                self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.RUMBLE)
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
                match self.current_state:
                    case GameState.INIT_PVP:
                        self.init_pvp()
                    case GameState.PVP_MATCH_LOOP:
                        self.match_loop()
                    case GameState.PVP_GAME_FINISH:
                        self.match_finish()
                    case GameState.ERROR_STATE:
                        self.error_handler.handler_errors()
            except Exception as e:
                logging.error(f'Something went wrong: {e}')
                state = self.error_handler.handler_errors()
                self.set_game_state(state)
