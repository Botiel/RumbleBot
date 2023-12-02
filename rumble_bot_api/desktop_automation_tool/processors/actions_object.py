from rumble_bot_api.desktop_automation_tool.utils.data_objects import Rect, ImagePosition, Position
from rumble_bot_api.desktop_automation_tool.processors.window_object import WindowObject
import pyautogui
from typing import Union
from time import sleep

Element = Union[Rect, ImagePosition, Position]


class Actions:

    def __init__(self, window: WindowObject):
        self.window = window

    @staticmethod
    def check_element(element: Element) -> tuple[int, int]:
        if isinstance(element, Position) or isinstance(element, ImagePosition):
            x = element.x
            y = element.y
        elif isinstance(element, Rect):
            x = element.center.x
            y = element.center.y
        else:
            raise ValueError('Wrong type of element')

        return x, y

    def click(
            self,
            element: Element,
            timeout_before_action: float = 0,
            timeout_after_action: float = 0,
            duration: float = 0,
    ) -> None:
        x, y = self.check_element(element)
        self.window.action(pyautogui.click, "click", x, y, timeout_before_action, timeout_after_action, duration)

    def move_to(
            self,
            element: Element,
            timeout_before_action: float = 0,
            timeout_after_action: float = 0,
            duration: float = 0
    ) -> None:
        x, y = self.check_element(element)
        self.window.action(pyautogui.moveTo, "move to", x, y, timeout_before_action, timeout_after_action, duration)

    def hold(
            self,
            element: Element,
            timeout_before_action: float = 0,
            timeout_after_action: float = 0,
            duration: float = 0
    ) -> None:
        x, y = self.check_element(element)
        self.window.action(pyautogui.mouseDown, "hold", x, y, timeout_before_action, timeout_after_action, duration)

    def release(
            self,
            element: Element,
            timeout_before_action: float = 0,
            timeout_after_action: float = 0,
            duration: float = 0
    ) -> None:
        x, y = self.check_element(element)
        self.window.action(pyautogui.mouseUp, "release", x, y, timeout_before_action, timeout_after_action, duration)

    def scroll_vertical(self, y_axis: int, duration: float = 0) -> None:
        x, y = self.window.get_window_screen_center()
        self.window.move_to(x, y)
        sleep(0.25)
        pyautogui.drag(0, y_axis, duration)

    def scroll_horizontal(self, x_axis: int, duration: float = 0) -> None:
        x, y = self.window.get_window_screen_center()
        self.window.move_to(x, y)
        sleep(0.25)
        pyautogui.drag(x_axis, 0, duration)

    def drag_and_drop(
            self,
            element: Element,
            drop_position: Position,
            timeout_before_moving: float = 0,
            timeout_before_dropping: float = 0,
            wait_after_drop: float = 0,
            drag_duration: float = 0
    ) -> None:
        self.hold(element)
        self.move_to(
            drop_position,
            timeout_before_moving,
            timeout_before_dropping,
            drag_duration
        )
        pyautogui.mouseUp()
        sleep(wait_after_drop)

