from rumble_bot_api.desktop_automation_tool.processors.window_object import WindowObject
from rumble_bot_api.desktop_automation_tool.processors.image_processing import ImageProcessing
from rumble_bot_api.desktop_automation_tool.processors.tesseract import Tesseract
from rumble_bot_api.desktop_automation_tool.processors.actions_object import Actions
from rumble_bot_api.desktop_automation_tool.utils.common import load_yaml_file
from pathlib import Path
import logging


class Processor:

    def __init__(self, yaml_file: str | Path):
        self.yaml_file = yaml_file
        self.yaml_config = load_yaml_file(yaml_file)

        logging.info('[Processors Loader] Setting up Processor Object')
        self.window = WindowObject(self.yaml_config)
        self.tesseract = Tesseract(self.window, self.yaml_config)
        self.image_processing = ImageProcessing(self.window, self.yaml_config)
        self.actions = Actions(self.window, self. tesseract)
