import logging
from time import sleep
from rumble_bot_api.desktop_automation_tool import Position, Processor, Region
from rumble_bot_api.predictor.predictor_object import Predictor
import rumble_bot_api.bot_core.utils.custom_exceptions as ex


GOLD_REGION = Region(
    top_left=Position(x=330, y=970),
    bottom_right=Position(x=380, y=1015)
)


class GoldHandler:

    def __init__(self, processor: Processor):
        self.processor = processor
        self.predictor = Predictor(processor.window, processor.yaml_config)

    def check_for_gold_ore_get_positions(self) -> list[Position] | None:
        logging.info('[Drop Handler] Checking for gold ore')

        positions = self.predictor.predict(model_name='gold')

        if not positions:
            logging.info('[Drop Handler] Gold ores not found')
            return

        logging.debug(f'[Drop Handler] Found gold ores: {positions}')
        return positions

    def get_current_gold_on_bar(self, region: Region = GOLD_REGION) -> int:

        for threshold in [210, 200, 190, 180, 170, 160]:
            text = self.processor.tesseract.extract_strings_from_window_image(
                threshold=threshold,
                specific_region=region,
                only_text=True
            )

            for item in text:
                if item in [str(x) for x in range(11)]:
                    return int(item)

        raise ex.ElementNotFoundException

    def wait_until_enough_gold(self, gold: int) -> None:
        logging.info(f'[Drop Handler] Waiting for [{gold}] gold to play mini')

        interval = 0.5
        time_elapsed = 0
        total_time = 18
        current_gold = self.get_current_gold_on_bar()

        if current_gold == gold:
            return

        while time_elapsed < total_time:

            current = self.get_current_gold_on_bar()

            if current:
                logging.debug(f'[Drop Handler] Current gold: {current}')
                if current >= gold:
                    logging.debug(f'[Drop Handler] There is enough gold: {current}')
                    return

            sleep(interval)
            time_elapsed += interval
