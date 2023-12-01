import logging
from typing import Literal
import cv2
import pytesseract
from pytesseract import Output
import os
from time import sleep, time
from desktop_automation_tool.utils.custom_exceptions import ElementNotFoundException
from desktop_automation_tool.utils.data_objects import Rect, Region, StringElement
from desktop_automation_tool.utils.common import get_folder
from desktop_automation_tool.processors.window_object import WindowObject


class Tesseract:

    def __init__(self, window: WindowObject, yaml_config: dict):
        self.window = window
        self._yaml_config = yaml_config
        self._psm = 6
        self._save_image = False
        self.set_tesseract_path(yaml_config.get('tesseract_path'))

    @staticmethod
    def set_tesseract_path(tesseract_path: str) -> None:

        if not tesseract_path:
            raise ValueError('[Tesseract] Tesseract path is not set, check config.ini file')

        if not os.path.exists(tesseract_path):
            raise FileNotFoundError(f'[Tesseract] Tesseract cmd file not found at path: {tesseract_path}')

        logging.info(f'[Tesseract] Loading Tesseract from Path: {tesseract_path}')
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def set_psm(self, psm: int) -> None:
        logging.info(f'[Tesseract] Setting PSM value to: {psm}')
        self._psm = psm

    def set_save_image_on(self) -> None:
        logging.info('[Tesseract] Image saving is ON')
        self._save_image = True

    def set_save_image_off(self) -> None:
        logging.info('[Tesseract] Image saving is OFF')
        self._save_image = False

    def extract_strings_from_window_image(
            self,
            threshold: int,
            specific_region: Region = None,
            only_text: bool = False,
    ) -> dict:
        """

        :param only_text: bool -> getting all data or only text data
        :param threshold: int [0 - 250]
        :param specific_region: Region object contains top left and bottom right coordinates
        :return:
        """

        logging.info('[Tesseract] Extracting strings from screenshot')

        if specific_region:
            image = self.window.get_window_screenshot(specific_region)
        else:
            image = self.window.get_window_screenshot()

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresholded_image = cv2.threshold(gray_image, threshold, 255, cv2.THRESH_BINARY)

        if self._save_image:
            output = get_folder(self._yaml_config, 'output')
            file = output / 'thresholded_tesseract_screenshot.png'
            cv2.imwrite(str(file), thresholded_image)

        data = pytesseract.image_to_data(thresholded_image, output_type=Output.DICT, config=f'--psm {self._psm}')

        return data if not only_text else data['text']

    def extract_string_coordinates_from_tesseract_data(
            self,
            string: str,
            threshold: int,
            exact_match: bool,
            region: Region = None
    ) -> list[Rect]:

        data = self.extract_strings_from_window_image(threshold, region)

        extracted_text = data.get('text')

        logging.info(f'f[Tesseract] Extracting string coordinates: {string}')
        extracted = []
        for i, text in enumerate(extracted_text):

            if exact_match:
                condition = text == string
            else:
                condition = string.lower() in text.lower()

            if condition:
                temp = Rect(
                    x=data['left'][i],
                    y=data['top'][i],
                    width=data['width'][i],
                    height=data['height'][i],
                    string=data['text'][i]
                )
                extracted.append(temp)

        return extracted

    def check_if_string_is_visible_on_screen(self, string: str, threshold: int, exact_match: bool) -> bool:
        logging.debug(f'[Tesseract] Checking if element is visible: {string}')
        data = self.extract_strings_from_window_image(threshold)
        text = data.get('text')

        if exact_match:
            is_text = list(filter(lambda x: x == string, text))
        else:
            is_text = list(filter(lambda x: string.lower() in x.lower(), text))

        if is_text:
            logging.debug(f'[Tesseract] element is visible: {string}')
            return True

        logging.debug(f'[Tesseract] element is NOT visible: {string}')
        return False

    def get_element(self, string_element: StringElement) -> list[Rect]:
        return self.extract_string_coordinates_from_tesseract_data(
            string_element.string,
            string_element.threshold,
            string_element.exact_match,
            string_element.region
        )

    def check_if_element_is_visible_on_screen(self, string_element: StringElement) -> bool:
        return self.check_if_string_is_visible_on_screen(
            string_element.string,
            string_element.threshold,
            string_element.exact_match
        )

    def wait_for_element(
            self,
            element: StringElement,
            timeout: float = 5,
            intervals: float = 0.5,
    ) -> list[Rect]:
        logging.info(f'Waiting for element: {element.string}')
        start_time = time()
        while time() - start_time < timeout:
            is_visible = self.check_if_element_is_visible_on_screen(element)
            if is_visible:
                locations = self.get_element(element)
                if locations:
                    logging.info(f'[Tesseract] Element Found: {element.string}')
                    return locations
            sleep(intervals)
        logging.info(f'[Tesseract] Did not find element: {element.string}')
        raise ElementNotFoundException

    def wait_for_element_state(
            self,
            element: StringElement,
            state: Literal['visible', 'hidden'],
            timeout: float = 5,
            intervals: float = 0.5,
    ) -> None:
        logging.info(f'[Tesseract] Waiting for element state: {element.string} | {state}')
        start_time = time()
        while time() - start_time < timeout:
            is_visible = self.check_if_element_is_visible_on_screen(element)
            if is_visible and state == 'visible' or not is_visible and state == 'hidden':
                return
            sleep(intervals)
        raise ElementNotFoundException
