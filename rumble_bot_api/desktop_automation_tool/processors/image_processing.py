import cv2
import numpy as np
import logging
from rumble_bot_api.desktop_automation_tool.utils.common import get_output_folder
from rumble_bot_api.desktop_automation_tool.processors.window_object import WindowObject
from rumble_bot_api.desktop_automation_tool.utils.data_objects import ImageElement, Region, ImagePosition
from skimage.metrics import structural_similarity as ssim


class ImageProcessing:

    def __init__(self, window: WindowObject):
        self.window = window
        self._save_image = False
        self._output_folder = get_output_folder()

    def set_save_image_on(self) -> None:
        logging.info('[Image Processing] Image saving is ON')
        self._save_image = True

    def set_save_image_off(self) -> None:
        logging.info('[Image Processing] Image saving is OFF')
        self._save_image = False

    def find_object_on_screen_get_coordinates(
            self,
            image_path: str,
            specific_region: Region = None,
    ) -> tuple[int, int, float]:

        logging.debug('[Image Processing] Searching for object on screen location')

        image_object = cv2.imread(image_path)
        image_screen = self.window.get_window_screenshot(specific_region)

        gray_object = cv2.cvtColor(image_object, cv2.COLOR_BGR2GRAY)
        gray_screen = cv2.cvtColor(image_screen, cv2.COLOR_BGR2GRAY)

        result = cv2.matchTemplate(gray_screen, gray_object, cv2.TM_CCOEFF_NORMED)

        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        top_left = max_loc
        h, w = gray_object.shape
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(image_screen, top_left, bottom_right, (0, 255, 0), 2)

        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)
        found_object = gray_screen[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        matching_score = ssim(gray_object, found_object)

        if self._save_image:
            output = self._output_folder
            cv2.imwrite(str(output / 'detected_object.jpg'), image_screen)

        return center[0], center[1], matching_score

    def find_element(self, element: ImageElement) -> ImagePosition | None:
        res = self.find_object_on_screen_get_coordinates(image_path=element.path, specific_region=element.region)
        return ImagePosition(x=res[0], y=res[1], ssim=res[2]) if res else None

    def wait_for_image(
            self,
            element: ImageElement,
            timeout: float = 5,
            intervals: float = 0.5
    ) -> ImagePosition | None:

        timer = 0
        while timer < timeout:
            res = self.find_object_on_screen_get_coordinates(image_path=element.path, specific_region=element.region)
            if res[2] >= element.ssim:
                return ImagePosition(x=res[0], y=res[1], ssim=res[2])
            timer += intervals

    def find_colors_in_specific_region_on_screen(
            self,
            hex_color: str,
            specific_region: Region,
            threshold: int = 10,
    ) -> bool:
        logging.debug(f'[Image Processing] Searching for color on screen location: {hex_color}')

        image = self.window.get_window_screenshot(specific_region)
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        bgr_color = np.uint8([[[int(hex_color[4:6], 16), int(hex_color[2:4], 16), int(hex_color[0:2], 16)]]])
        hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)[0][0]

        diff_h = np.abs(hsv_image[:, :, 0] - hsv_color[0])
        diff_s = np.abs(hsv_image[:, :, 1] - hsv_color[1])
        diff_v = np.abs(hsv_image[:, :, 2] - hsv_color[2])

        color_found = np.logical_and.reduce((diff_h <= threshold, diff_s <= threshold, diff_v <= threshold))

        return True if np.any(color_found) else False
