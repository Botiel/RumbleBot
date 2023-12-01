import logging
import cv2
import pyautogui
from time import sleep
import numpy as np
from numpy import ndarray
import pygetwindow
import subprocess
import sys
from typing import Optional
from pygetwindow import PyGetWindowException, Win32Window
from desktop_automation_tool.utils.data_objects import Region
from desktop_automation_tool.utils.custom_exceptions import WindowNotFoundException
from desktop_automation_tool.utils.common import get_folder


class WindowObject:

    def __init__(self, yaml_config: dict):
        self._yaml_config = yaml_config
        self.window_title = yaml_config.get('window_title')
        self.executable_path = yaml_config.get('window_path')
        self.window: Optional[Win32Window] = None

    def set_window(self) -> None:
        windows = pygetwindow.getAllWindows()
        try:
            window = list(filter(lambda x: x.title == self.window_title, windows))[0]
        except IndexError:
            raise WindowNotFoundException

        logging.info(f'[Window] Setting window object')
        self.window = window

    def run_emulator(self) -> None:
        try:
            subprocess.Popen(
                [self.executable_path],
                shell=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                close_fds=True
            )
            print(f"Executable ran successfully: {self.executable_path}")

        except subprocess.CalledProcessError as e:
            print(f"Error running the executable: {e}")
            sys.exit(1)

    def terminate_window(self) -> None:
        self.window.close()
        logging.info('[Window] Closing Window')

    def check_and_activate_window(self) -> None:
        logging.info('>>> Checking if Emulator Window is activated')
        if self.window.isActive:
            logging.info('>>> Emulator already active')
            return

        try:
            self.window.activate()
        except PyGetWindowException:
            pass
        sleep(1)
        logging.info('>>> Emulator Window: Activated')

    def get_window_screenshot(
            self,
            specific_region: Region = None,
            save_image: bool = False
    ) -> ndarray:
        """

        :param specific_region: 2 pairs of (x, y) box region coordinates
        :param save_image: True | False
        :return:
        """

        # Taking emulator's screen screenshot and adjusting coordinates
        w = self.window
        x, y, width, height = w.left, w.top, w.width, w.height
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        if specific_region:
            region_points = np.array(specific_region.get_full_region(), np.int32)
            mask = np.zeros((screenshot.shape[0], screenshot.shape[1]), dtype=np.uint8)
            cv2.fillPoly(mask, [region_points], 255)
            screenshot[mask == 0] = [0, 0, 0]

        if save_image:
            output = get_folder(self._yaml_config, 'output')
            file = output / 'window_screenshot.png'
            cv2.imwrite(str(file), screenshot)
            logging.info(f'[Window] Saved image to: {file}')

        return screenshot

    def get_window_screen_center(self) -> tuple:
        screenshot = self.get_window_screenshot()
        height, width, _ = screenshot.shape
        center_x = width // 2
        center_y = height // 2
        return center_x, center_y

    def action(
            self,
            action: pyautogui,
            name: str,
            x: int = 0,
            y: int = 0,
            timeout_before_action: float = 0,
            timeout_after_action: float = 0,
            duration: float = 0
    ) -> None:

        # Normalizing coordinates to window screen
        _x = self.window.topleft.x + x
        _y = self.window.topleft.y + y

        logging.info(f'[Mouse Action] {name} at ({_x}, {_y})')
        sleep(timeout_before_action)
        action(x=_x, y=_y, duration=duration)
        sleep(timeout_after_action)

    def move_to(
            self,
            x: int = 0,
            y: int = 0,
            timeout_before_action: float = 0,
            timeout_after_action: float = 0,
            duration: float = 0
    ) -> None:
        self.action(
            pyautogui.moveTo,
            'move to',
            x,
            y,
            timeout_before_action,
            timeout_after_action,
            duration
        )
