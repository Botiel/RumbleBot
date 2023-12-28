import logging
from time import sleep, time
from rumble_bot_api.bot_core.string_assets import STRING_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import GameState
from rumble_bot_api.bot_core.handlers.base_handler import BaseHandler
from rumble_bot_api.bot_core.utils.custom_exceptions import NoMinisOnBoardException, GoldNotFoundException
from rumble_bot_api.bot_core.handlers.drop_handler import DropHandler
from rumble_bot_api.bot_core.utils.common import ACT_2_ELEMENT
from rumble_bot_api.desktop_automation_tool.utils.data_objects import Position
from rumble_bot_api.bot_core.mini_assets import MINI_ASSETS as MINIS


class BossHandler(BaseHandler):

    def __init__(self, drop_handler: DropHandler):
        super().__init__(drop_handler)
        self.set_game_mode('boss')

        self._boss = STRING_ASSETS.DREADNAUGHT
        self.drop_handler.set_lineup([
                MINIS.quilboar.skill_0,
                MINIS.pilot.skill_1,
                MINIS.worgen.skill_1,
                MINIS.blizzard.skill_1,
                MINIS.whelp_eggs.skill_1,
                MINIS.execute.skill_0
        ])

    def init_boss(self) -> None:
        logging.info('[Boss Handler] Initializing Boss Mission')

        position = self.image_processing.find_element(ACT_2_ELEMENT)
        if position and position.ssim > ACT_2_ELEMENT.ssim:
            self.actions.click(position)
        else:

            for _ in range(3):
                self.actions.scroll_horizontal(500, duration=0.2)

            for _ in range(2):
                self.actions.scroll_vertical(500, duration=0.2)

            self.actions.scroll_horizontal(-500, duration=0.2)
            self.actions.scroll_vertical(-500, duration=0.2)

            sleep(1)
            position = self.image_processing.find_element(ACT_2_ELEMENT)
            if position and position.ssim > ACT_2_ELEMENT.ssim:
                self.actions.click(position)

        self.set_game_state(GameState.PRE_BOSS_MATCH)

    def pre_match(self) -> None:
        logging.info('[Boss Handler] Starting Boss Mission')
        self.actions.wait_and_try_click_string_element(self._boss, timeout=10)
        self.actions.wait_and_try_click_string_element(STRING_ASSETS.BOSS_PLAY)
        self.wait_for_load_state()
        self.actions.wait_and_try_click_string_element(STRING_ASSETS.TAP, timeout=20)

        self.set_game_state(GameState.BOSS_MATCH_LOOP)

    def match_loop(self) -> None:
        logging.info('[Boss Handler] Starting a Boss Match')

        bottom = Position(x=779, y=507)
        top = Position(x=656, y=389)
        top2 = Position(x=600, y=310)
        middle = Position(x=640, y=475)

        self.tesseract.wait_for_element_state(STRING_ASSETS.START, state='visible', timeout=20)

        for _ in range(2):
            self.actions.scroll_vertical(500, duration=0.1)

        self.actions.wait_and_try_click_string_element(STRING_ASSETS.START)

        self.wait_for_match_to_start()

        while True:

            try:
                current = self.drop_handler.get_current_minis_on_board()
                if not current:
                    raise NoMinisOnBoardException

                minis_li = list(current)

                if MINIS.quilboar.name in minis_li and MINIS.worgen.name in minis_li:
                    self.drop_handler.gold_handler.wait_until_enough_gold(5)
                    quilboar = current.get(MINIS.quilboar.name)
                    worgen = current.get(MINIS.worgen.name)
                    self.drop_handler.drop_mini(quilboar, bottom)
                    self.drop_handler.drop_mini(worgen, top2)

                elif MINIS.pilot.name in minis_li:
                    pilot = current.get(MINIS.pilot.name)
                    self.drop_handler.drop_mini(pilot, top)

                elif MINIS.whelp_eggs.name in minis_li:
                    whelp_eggs = current.get(MINIS.whelp_eggs.name)
                    self.drop_handler.drop_mini(whelp_eggs, bottom)

                else:
                    if MINIS.blizzard.name in minis_li:
                        blizzard = current.get(MINIS.blizzard.name)
                        self.drop_handler.drop_mini(blizzard, middle)
                    elif MINIS.execute.name in minis_li:
                        execute = current.get(MINIS.execute.name)
                        self.drop_handler.drop_mini(execute, middle)

            except (GoldNotFoundException, NoMinisOnBoardException):
                self.set_game_state(GameState.BOSS_GAME_FINISH)
                return

            finally:
                if self.match_error_check():
                    return

    def match_finish(self) -> None:
        logging.info('[Match Handler] Navigating to a new game')

        is_continue = False
        is_try_again = False

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
            self.set_game_state(GameState.BOSS_MATCH_LOOP)
            return

        if is_continue:
            self.actions.click_string_element_until_hidden(STRING_ASSETS.CONTINUE)
            self.wait_for_load_state()
            self.set_game_state(GameState.PRE_BOSS_MATCH)

    def main_loop(self) -> None:

        self.set_game_state(GameState.INIT_BOSS)

        while True:
            try:
                match self._current_state:
                    case GameState.INIT_BOSS:
                        self.init_boss()
                    case GameState.PRE_BOSS_MATCH:
                        self.pre_match()
                    case GameState.BOSS_MATCH_LOOP:
                        self.match_loop()
                    case GameState.BOSS_GAME_FINISH:
                        self.match_finish()
                    case GameState.ERROR_STATE:
                        self.handler_errors()
            except Exception as e:
                logging.error(f'Something went wrong: {e}')
                self.set_game_state(GameState.ERROR_STATE)
