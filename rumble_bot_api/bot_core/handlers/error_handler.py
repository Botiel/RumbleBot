import logging
from rumble_bot_api.desktop_automation_tool.utils.custom_exceptions import ElementNotFoundException
from rumble_bot_api.desktop_automation_tool.processors_loader import Processor
from rumble_bot_api.bot_core.string_assets import STRING_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import GameState
from rumble_bot_api.bot_core.handlers.base_handler import BaseHandler
from time import sleep
import sys


class ErrorHandler(BaseHandler):

    def __init__(self, processor: Processor, mode: str):
        super().__init__(processor)
        self.mode = mode

    def check_for_error_message(self) -> GameState | None:
        logging.info('[Error Handler] Checking for error message')

        try:
            self.tesseract.wait_for_element_state(STRING_ASSETS.ERROR, state='visible', timeout=3)
        except ElementNotFoundException:
            logging.info('[Error Handler] No error message')
            return

        logging.info('[Error Handler] Error found, handling error!')
        self.actions.click_string_element_until_hidden(STRING_ASSETS.OK)
        self.wait_for_load_state()

        if self.mode == 'quests':
            return GameState.INIT_QUESTS

        if self.mode == 'pvp':
            return GameState.INIT_PVP

    def check_if_game_crashed(self) -> GameState | None:
        logging.info('[Error Handler] Checking if the game crashed')

        try:
            location = self.tesseract.wait_for_element(STRING_ASSETS.RUMBLE, timeout=3)[0]
        except ElementNotFoundException:
            logging.error('[Error Handler] Game did not crash')
            return

        logging.error('[Error Handler] Game crashed, trying to login!')
        self.actions.click(location)
        self.wait_for_load_state()

        if self.mode == 'quests':
            return GameState.INIT_QUESTS

        if self.mode == 'pvp':
            return GameState.INIT_PVP

    def find_current_game_states(self) -> GameState | None:
        logging.error('[Error Handler] Trying to find current state')

        if self.mode == 'quests':
            elements_to_check = [
                (STRING_ASSETS.START, GameState.QUESTS_MATCH_LOOP),
                (STRING_ASSETS.TRY_AGAIN, GameState.QUESTS_PRE_MATCH),
                (STRING_ASSETS.PLAY, GameState.QUESTS_PRE_MATCH),
                (STRING_ASSETS.CONTINUE, GameState.QUESTS_GAME_FINISH),
                (STRING_ASSETS.CLAIM, GameState.INIT_QUESTS),
                (STRING_ASSETS.QUEST, GameState.INIT_QUESTS),
            ]

        elif self.mode == 'pvp':
            elements_to_check = [
                (STRING_ASSETS.CONTINUE, GameState.PVP_GAME_FINISH),
                (STRING_ASSETS.CLAIM, GameState.INIT_PVP),
                (STRING_ASSETS.RUMBLE_PVP, GameState.INIT_PVP),
                (STRING_ASSETS.PVP, GameState.INIT_PVP),
            ]

        else:
            logging.error(f'No such game mode: {self.mode}')
            sys.exit(1)

        for element, state in elements_to_check:
            is_clicked = self.actions.wait_and_try_click_string_element(element, 1, 1, ignore_exception=True)
            if is_clicked:
                return state
        return

    def reopen_emulator(self) -> GameState | None:
        logging.info('[Error Handler] Could not handle errors, re-opening emulator')
        self.window.terminate_window()
        sleep(30)
        self.window.run_window()
        sleep(20)
        self.window.set_window()
        location = self.tesseract.wait_for_element(STRING_ASSETS.RUMBLE, 45)[0]
        self.actions.click(location, timeout_before_action=1)
        self.wait_for_load_state(45)

        if self.mode == 'quests':
            return GameState.INIT_QUESTS

        if self.mode == 'pvp':
            return GameState.INIT_PVP

    def handler_errors(self) -> GameState:
        logging.error('[Error Handler] error handling loop started')

        while True:
            state = self.check_for_error_message()
            if state:
                return state

            state = self.check_if_game_crashed()
            if state:
                return state

            state = self.find_current_game_states()
            if state:
                return state

            self.handle_level_up()


if __name__ == '__main__':
    from rumble_bot_api.bot_core.utils.common import find_root_dir, set_logger
    set_logger()
    root = find_root_dir()
    p = Processor(root / 'config.yaml')
    p.window.set_window()
    e = ErrorHandler(p, 'quests')
    e.reopen_emulator()
