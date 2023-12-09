import logging
from time import sleep
from rumble_bot_api.desktop_automation_tool import Position, Processor, Region
from rumble_bot_api.predictor.predictor_object import Predictor
from rumble_bot_api.bot_core.utils.custom_exceptions import GoldNotFoundException


GOLD_REGION = Region(top_left=Position(x=330, y=970), bottom_right=Position(x=380, y=1015))


class GoldHandler:

    def __init__(self, processor: Processor):
        self.processor = processor
        self.predictor = Predictor(processor.window, processor.yaml_config)

    def check_for_gold_ore_get_positions(self) -> list[Position] | None:
        logging.info('[Gold Handler] Checking for gold ore')

        prediction = self.predictor.predict(conf=0.85)
        gold_positions = [p.center for p in prediction.goldmine]

        if not gold_positions:
            logging.info('[Gold Handler] Gold ores not found')
            return

        logging.debug(f'[Gold Handler] Found gold ores: {gold_positions}')
        return gold_positions

    def get_current_gold_on_bar(self, region: Region = GOLD_REGION) -> int:
        logging.debug('[Gold Handler] Checking for current gold')

        for threshold in [i for i in range(220, 175, -5)]:

            text = self.processor.tesseract.extract_strings_from_window_image(
                threshold=threshold,
                specific_region=region,
                only_text=True
            )

            for item in text:
                if item in [str(x) for x in range(11)]:
                    logging.debug(f'[Gold Handler] Current gold: {item}')
                    return int(item)

            sleep(0.2)

        logging.error(f'[Gold Handler] did not find gold image')
        raise GoldNotFoundException

    def wait_until_enough_gold(self, gold: int) -> None:
        logging.info(f'[Gold Handler] Waiting for [{gold}] gold to play mini')

        interval = 0.5
        time_elapsed = 0
        total_time = 18

        while time_elapsed < total_time:

            current = self.get_current_gold_on_bar()

            if current:
                if current >= gold:
                    logging.debug(f'[Gold Handler] There is enough gold: {current}')
                    return

            sleep(interval)
            time_elapsed += interval
