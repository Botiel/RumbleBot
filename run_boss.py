from rumble_bot_api.bot_core.utils.common import set_logger
from rumble_bot_api import Processor, DropHandler, BossHandler, Predictor
from config import TESSERACT_PATH, EMULATOR_PATH, EMULATOR_TITLE


def main() -> None:

    set_logger(20)

    processor = Processor()
    processor.set_configurations(TESSERACT_PATH, EMULATOR_PATH, EMULATOR_TITLE)

    predictor = Predictor(processor.window)
    drop_handler = DropHandler(processor, predictor)
    boss = BossHandler(drop_handler)

    boss.main_loop()


if __name__ == '__main__':
    main()
