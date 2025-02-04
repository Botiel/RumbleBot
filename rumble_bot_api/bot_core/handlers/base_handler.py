import logging
from time import sleep
import sys
from rumble_bot_api.bot_core.utils.custom_exceptions import GoldNotFoundException
from rumble_bot_api.desktop_automation_tool.utils.custom_exceptions import ElementNotFoundException
from rumble_bot_api.bot_core.string_assets import STRING_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import GameState
from rumble_bot_api.bot_core.utils.common import LEVELUP_STAR
from rumble_bot_api.bot_core.handlers.drop_handler import DropHandler
from typing import Literal


class BaseHandler:

    def __init__(self, drop_handler: DropHandler):
        self.drop_handler = drop_handler
        self.window = self.drop_handler.processor.window
        self.tesseract = self.drop_handler.processor.tesseract
        self.image_processing = self.drop_handler.processor.image_processing
        self.actions = self.drop_handler.processor.actions

        self._current_state = None
        self._mode = None

    # ------------------------------------------------- SETTERS --------------------------------------------------------
    def set_game_state(self, state: GameState) -> None:
        logging.info(f'[Base Handler] state is set to: {state.value}')
        self._current_state = state

    def set_game_mode(self, mode: Literal['quests', 'pvp', 'boss']) -> None:

        if mode not in ['quests', 'pvp', 'boss']:
            raise ValueError(f'no such game mode: {mode}')

        logging.info(f'[Base Handler] game mode is set to: {mode}')
        self._mode = mode

    # ------------------------------------------------- GENERAL --------------------------------------------------------
    def wait_for_load_state(self) -> None:
        logging.info('[Loading State] Loading...')
        self.tesseract.wait_for_element_state(
            element=STRING_ASSETS.LOADING,
            timeout=30,
            state='visible'
        )
        self.tesseract.wait_for_element_state(
            element=STRING_ASSETS.LOADING,
            timeout=45,
            state='hidden'
        )
        logging.info('[Loading State] Done!')

    def handle_level_up(self) -> None:
        logging.info('[Base Handler] handling level up')
        result = self.image_processing.wait_for_image(LEVELUP_STAR, timeout=15)
        if result:
            self.actions.click(result)

    def wait_for_match_to_start(self, timeout: float = 40, intervals: float = 0.5) -> None:
        logging.info(f'[Base Handler] Waiting for the match to start: {self._mode}')

        timer = 0

        while True:

            result = self.drop_handler.get_current_minis_on_board()
            if not result:
                sleep(intervals)
                timer += intervals
            else:
                break

            if timer == timeout:
                raise Exception(f'[Base Handler] Match did not start after {timer} seconds')

    # ---------------------------------------------- ERROR HANDLING ----------------------------------------------------
    def check_for_error_message(self) -> GameState | None:
        logging.info('[Error Handler] Checking for error message')

        is_error = False

        try:
            self.tesseract.wait_for_element_state(STRING_ASSETS.ERROR, state='visible', timeout=3)
        except ElementNotFoundException:
            logging.info('[Error Handler] No Error message')
        else:
            is_error = True

        try:
            self.tesseract.wait_for_element_state(STRING_ASSETS.FAILED, state='visible', timeout=3)
        except ElementNotFoundException:
            logging.info('[Error Handler] No Failed message')
        else:
            is_error = True

        if not is_error:
            return

        logging.info('[Error Handler] Error found, handling error!')
        self.actions.click_string_element_until_hidden(STRING_ASSETS.OK)
        self.wait_for_load_state()

        if self._mode == 'quests':
            return GameState.INIT_QUESTS

        if self._mode == 'pvp':
            return GameState.INIT_PVP

        if self._mode == 'boss':
            return GameState.PRE_BOSS_MATCH

    def check_if_game_crashed(self) -> GameState | None:
        logging.info('[Error Handler] Checking if the game crashed')

        try:
            self.tesseract.wait_for_element(STRING_ASSETS.TOOLS, timeout=3)[0]
        except ElementNotFoundException:
            logging.error('[Error Handler] Game did not crash')
            return

        logging.error('[Error Handler] Game crashed, trying to login!')
        locations = self.tesseract.wait_for_element(STRING_ASSETS.RUMBLE, timeout=3)
        for loc in locations:
            self.actions.click(loc)
        self.wait_for_load_state()

        if self._mode == 'quests':
            return GameState.INIT_QUESTS

        if self._mode == 'pvp':
            return GameState.INIT_PVP

        if self._mode == 'boss':
            return GameState.PRE_BOSS_MATCH

    def find_current_game_states(self) -> GameState | None:
        logging.error('[Error Handler] Trying to find current state')

        if self._mode == 'quests':
            elements_to_check = [
                (STRING_ASSETS.START, GameState.QUESTS_MATCH_LOOP),
                (STRING_ASSETS.TRY_AGAIN, GameState.QUESTS_GAME_FINISH),
                (STRING_ASSETS.CONTINUE, GameState.QUESTS_GAME_FINISH),
                (STRING_ASSETS.CLAIM, GameState.INIT_QUESTS),
                (STRING_ASSETS.CLAIM_AFTER_QUEST, GameState.INIT_QUESTS),
                (STRING_ASSETS.QUEST, GameState.INIT_QUESTS),
            ]

        elif self._mode == 'boss':
            elements_to_check = [
                (STRING_ASSETS.START, GameState.BOSS_MATCH_LOOP),
                (STRING_ASSETS.TRY_AGAIN, GameState.BOSS_GAME_FINISH),
                (STRING_ASSETS.CONTINUE, GameState.BOSS_GAME_FINISH),
                (STRING_ASSETS.BOSS_PLAY, GameState.PRE_BOSS_MATCH),
                (STRING_ASSETS.PVP, GameState.INIT_BOSS),
                (STRING_ASSETS.BACK, GameState.PRE_BOSS_MATCH),
            ]

        elif self._mode == 'pvp':
            elements_to_check = [
                (STRING_ASSETS.CONTINUE, GameState.PVP_GAME_FINISH),
                (STRING_ASSETS.CLAIM, GameState.INIT_PVP),
                (STRING_ASSETS.RUMBLE_PVP, GameState.INIT_PVP),
                (STRING_ASSETS.PVP, GameState.INIT_PVP),
            ]

        else:
            logging.error(f'No such game mode: {self._mode}')
            sys.exit(1)

        for element, state in elements_to_check:
            try:
                self.tesseract.wait_for_element_state(element, state='visible', timeout=1.5)
            except ElementNotFoundException:
                continue
            else:
                return state

    def reopen_emulator(self) -> GameState | None:
        logging.info('[Error Handler] Could not handle errors, re-opening emulator')
        self.window.terminate_window()
        sleep(30)
        self.window.run_window()
        sleep(20)
        self.window.set_window()
        location = self.tesseract.wait_for_element(STRING_ASSETS.RUMBLE, 45)[0]
        self.actions.click(location, timeout_before_action=1)
        self.wait_for_load_state()

        if self._mode == 'quests':
            return GameState.INIT_QUESTS

        if self._mode == 'pvp':
            return GameState.INIT_PVP

    def handler_errors(self) -> None:
        logging.error('[Error Handler] error handling loop started')

        while True:

            state = self.check_for_error_message()
            if state:
                self.set_game_state(state)
                return

            state = self.check_if_game_crashed()
            if state:
                self.set_game_state(state)
                return

            state = self.find_current_game_states()
            if state:
                self.set_game_state(state)
                return

            self.handle_level_up()

    def match_error_check(self) -> bool:
        error = [
            self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.ERROR),
            self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.FAILED),
            self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.TOOLS)
        ]
        if any(error):
            self.set_game_state(GameState.ERROR_STATE)
            return True

        return False
