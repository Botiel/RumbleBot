from config import TESSERACT_PATH, EMULATOR_PATH, EMULATOR_TITLE
from rumble_bot_api import Processor
from pathlib import Path
from time import sleep
import keyboard
import sys
import os


ROOT = Path(__file__).resolve().parent
SCREENSHOTS = ROOT / 'screenshots'


def main() -> None:
    print('Setting up processor...')

    processor = Processor()
    processor.set_configurations(TESSERACT_PATH, EMULATOR_PATH, EMULATOR_TITLE)

    print('Process is ready...')

    while True:

        print('Taking a screenshot')
        if not os.path.exists(SCREENSHOTS):
            os.makedirs(SCREENSHOTS)

        processor.window.get_window_screenshot(save_image=True, generate_name=True, folder_path=SCREENSHOTS)

        if keyboard.is_pressed('q'):
            sys.exit(0)

        sleep(2)


if __name__ == '__main__':
    main()
