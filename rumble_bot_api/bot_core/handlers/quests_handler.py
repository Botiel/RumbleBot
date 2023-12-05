import logging
from random import choice
from time import sleep, time
from rumble_bot_api.desktop_automation_tool.processors_loader import Processor
from rumble_bot_api.bot_core.string_assets import STRING_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import GameState
from rumble_bot_api.bot_core.handlers.base_handler import BaseHandler
from rumble_bot_api.bot_core.handlers.error_handler import ErrorHandler
from rumble_bot_api.desktop_automation_tool.utils.custom_exceptions import ElementNotFoundException
from rumble_bot_api.bot_core.utils.custom_exceptions import NoMinisOnBoardException
from rumble_bot_api.bot_core.utils.data_objects import Node


class QuestsHandler(BaseHandler):

    def __init__(self, processor: Processor, lineup: list[Node], levelup_list: list[str]):
        super().__init__(processor)
        self.error_handler = ErrorHandler(processor, 'quests')
        self.lineup = lineup
        self.levelup_list = levelup_list

        self.drop_handler.set_game_mode('quests')
        self.drop_handler.set_quests_lineup(lineup)

    def match_mini_and_play_button_in_quest(self) -> None:
        logging.info('[Quests Handler] Matching minions in quest to buttons')

        new_li = [item.split('_')[0] for item in self.levelup_list]

        minis = self.tesseract.extract_many_string_coordinates_from_tesseract_data(new_li, 180, False)
        buttons = self.tesseract.wait_for_element(STRING_ASSETS.PLAY, 5)

        if not minis:
            logging.info('[Quests Handler] No minis from levelup list where found, choosing a random mini quest')
            btn = choice(buttons)
            self.actions.click(btn)
            return

        logging.debug(f'[Quests Handler] MINIS: {minis}')
        logging.debug(f'[Quests Handler] BUTTONS: {buttons}')

        btn_dict = {}
        for mini in minis:
            for btn in buttons:
                if mini.center.x // 100 == btn.center.x // 100:
                    btn_dict[mini.string] = btn

        logging.debug(f'[Quests Handler] MATCH BUTTONS: {btn_dict}')

        to_click = None
        for mini in new_li:
            for k, v in btn_dict.items():
                if mini.lower() == k.lower():
                    logging.info(f'[Quests Handler] Found a mini from levelup list: {k}: {v}')
                    to_click = v
                    break

        while self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.PLAY):
            self.actions.click(to_click, timeout_after_action=2)

    def init_quests(self) -> None:
        logging.info('[Quests Handler] Starting Quests')

        if self.actions.wait_and_try_click_string_element(STRING_ASSETS.CLAIM, 4, ignore_exception=True):
            self.handle_level_up()

        self.actions.wait_and_try_click_string_element(STRING_ASSETS.QUEST)

        if self.actions.wait_and_try_click_string_element(STRING_ASSETS.CLAIM, 2, ignore_exception=True):
            self.handle_level_up()
            self.actions.wait_and_try_click_string_element(STRING_ASSETS.QUEST)

        self.match_mini_and_play_button_in_quest()

        self.set_game_state(GameState.QUESTS_PRE_MATCH)

    def pre_match(self) -> None:
        logging.info('[Match Handler] Pre Match')

        self.wait_for_load_state()
        self.tesseract.wait_for_element_state(STRING_ASSETS.START, state='visible', timeout=45)

        self.drop_handler.calculate_drop_zones_for_quests()

        self.actions.wait_and_try_click_string_element(STRING_ASSETS.START)

        self.wait_for_match_to_start()

        self.set_game_state(GameState.QUESTS_MATCH_LOOP)

    def match_loop(self) -> None:
        logging.info('[Quests Handler] Starting a Quests Match')

        curr_zone = self.drop_handler.drop_zones.LEFT

        while True:
            for mini in self.lineup:
                logging.info(f'[Quests Handler] Next Mini in queue: {mini.name}')

                try:
                    is_dropped = self.drop_handler.drop_mini(mini.name, curr_zone)
                    if is_dropped:
                        self.drop_handler.drop_miner_for_quests()
                except (ElementNotFoundException, NoMinisOnBoardException):
                    # checking for the gold cost rectangle element and minis board
                    self.set_game_state(GameState.QUESTS_GAME_FINISH)
                    return

                if is_dropped:
                    if curr_zone == self.drop_handler.drop_zones.LEFT:
                        curr_zone = self.drop_handler.drop_zones.TOP
                    elif curr_zone == self.drop_handler.drop_zones.TOP:
                        curr_zone = self.drop_handler.drop_zones.RIGHT
                    else:
                        curr_zone = self.drop_handler.drop_zones.LEFT

            error = [
                self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.ERROR),
                self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.RUMBLE)

            ]
            if any(error):
                self.set_game_state(GameState.ERROR_STATE)
                return

    def match_finish(self) -> None:
        logging.info('[Match Handler] Navigating to a new game')

        is_continue = None
        is_try_again = None

        start_time = time()
        while time() - start_time < 15:
            is_continue = self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.CONTINUE)
            is_try_again = self.tesseract.check_if_element_is_visible_on_screen(STRING_ASSETS.TRY_AGAIN)
            sleep(0.5)
            if is_continue or is_try_again:
                break

        if not is_continue and not is_try_again:
            self.set_game_state(GameState.ERROR_STATE)
            return

        if is_try_again:
            self.actions.click_string_element_until_hidden(STRING_ASSETS.TRY_AGAIN)
            self.set_game_state(GameState.QUESTS_PRE_MATCH)
            return

        if is_continue:
            self.actions.click_string_element_until_hidden(STRING_ASSETS.CONTINUE)
            self.wait_for_load_state()
            self.set_game_state(GameState.INIT_QUESTS)

    def main_loop(self) -> None:

        self.set_game_state(GameState.INIT_QUESTS)

        while True:
            try:
                match self.current_state:
                    case GameState.INIT_QUESTS:
                        self.init_quests()
                    case GameState.QUESTS_PRE_MATCH:
                        self.pre_match()
                    case GameState.QUESTS_MATCH_LOOP:
                        self.match_loop()
                    case GameState.QUESTS_GAME_FINISH:
                        self.match_finish()
                    case GameState.ERROR_STATE:
                        self.error_handler.handler_errors()
            except Exception as e:
                logging.error(f'Something went wrong: {e}')
                state = self.error_handler.handler_errors()
                self.set_game_state(state)
