from rumble_bot_api.desktop_automation_tool.processors.window_object import WindowObject
from rumble_bot_api.desktop_automation_tool.processors.image_processing import ImageProcessing
from rumble_bot_api.desktop_automation_tool.processors.tesseract import Tesseract
from rumble_bot_api.desktop_automation_tool.processors.actions_object import Actions
import logging


class Processor:

    def __init__(self):
        logging.info('[Processor] Setting up Processor')
        self.window = WindowObject()
        self.tesseract = Tesseract(self.window)
        self.image_processing = ImageProcessing(self.window)
        self.actions = Actions(self.window, self. tesseract)

    def set_configurations(self, tesseract_path: str, window_path: str, window_title: str) -> None:
        logging.info('[Processor] Setting up configurations')
        self.window.set_window_title_and_object(window_title)
        self.window.set_executable_path(window_path)
        self.tesseract.set_tesseract_path(tesseract_path)
