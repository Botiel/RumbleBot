import logging
from time import sleep
from rumble_bot_api.desktop_automation_tool.utils.custom_exceptions import ElementNotFoundException
from rumble_bot_api.desktop_automation_tool.processors_loader import Processor
from rumble_bot_api.bot_core.handlers.drop_handler import DropHandler
from rumble_bot_api.bot_core.string_assets import STRING_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import GameState


class BaseHandler:

    def __init__(self, processor: Processor):
        self._processor = processor
        self.window = processor.window
        self.tesseract = processor.tesseract
        self.image_processing = processor.image_processing
        self.actions = processor.actions

        self.drop_handler = DropHandler(processor)

        self.current_state = None

    def set_game_state(self, state: GameState) -> None:
        logging.info(f'[Base Handler] state is set to: {state.value}')
        self.current_state = state

    def wait_for_load_state(self, wait_time: int = 45) -> None:
        logging.info('[Loading State] Loading...')
        self.tesseract.wait_for_element_state(
            element=STRING_ASSETS.LOADING,
            timeout=wait_time,
            state='visible'
        )
        self.tesseract.wait_for_element_state(
            element=STRING_ASSETS.LOADING,
            timeout=wait_time,
            state='hidden'
        )
        logging.info('[Loading State] Done!')

    def handle_level_up(self) -> None:
        logging.info('[Base Handler] handling level up')

        try:
            self.tesseract.wait_for_element_state(STRING_ASSETS.LEVEL_UP, 'visible', 7)
        except ElementNotFoundException:
            logging.info('[Base Handler] no level up...')
            return

        self.actions.click_string_element_until_hidden(STRING_ASSETS.LEVEL_UP)

    def wait_for_match_to_start(self, timeout: float = 40, intervals: float = 0.5) -> None:
        logging.info(f'[Base Handler] Waiting for the match to start: {self.drop_handler.game_mode}')
        timer = 0

        while True:

            try:
                self.drop_handler.gold_handler.get_current_gold_on_bar()

            except ElementNotFoundException:
                sleep(intervals)
                timer += intervals

                if timer == timeout:
                    raise Exception(f'[Base Handler] Match did not start after {timer} seconds')

                continue

            else:
                break
