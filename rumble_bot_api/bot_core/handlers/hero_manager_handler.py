import logging
from time import sleep
from rumble_bot_api.desktop_automation_tool.processors_loader import Processor
from rumble_bot_api.desktop_automation_tool.utils.data_objects import Position
from rumble_bot_api.bot_core.utils.common import HEROES_FOLDER, MAP_ELEMENT, COLLECTION_ELEMENT
from rumble_bot_api.bot_core.string_assets import STRING_ASSETS


HERO_BAR_POSITION = Position(x=500, y=150)
HEROES_IMAGE_SSIM = 0.8


class HeroManagerHandler:

    def __init__(self, processor: Processor):
        self.processor = processor
        self.heroes_dict = self.load_heroes()

    @staticmethod
    def load_heroes() -> dict:
        return {
            item.name.replace('hero_', '').replace('.png', ''): str(item)
            for item in HEROES_FOLDER.iterdir()
            if item.is_file() and item.name.endswith('.png')
        }

    def switch_hero(self, hero_name: str) -> None:

        hero_image_path = self.heroes_dict.get(hero_name)
        if not hero_image_path:
            raise ValueError(f'no such hero: {hero_name}')

        result = self.processor.image_processing.find_element(COLLECTION_ELEMENT)
        if result.ssim > COLLECTION_ELEMENT.ssim:
            self.processor.actions.click(result)

        self.processor.tesseract.wait_for_element_state(STRING_ASSETS.TROOPS, state='visible')

        for _ in range(3):
            self.processor.actions.scroll_horizontal(x_axis=-400, from_position=HERO_BAR_POSITION)

        sleep(1)

        is_clicked = False
        for _ in range(4):
            x, y, ssim = self.processor.image_processing.find_object_on_screen_get_coordinates(hero_image_path)
            logging.debug(f'HERO SSIM: {ssim}')
            if ssim > HEROES_IMAGE_SSIM:
                self.processor.actions.click(Position(x=x, y=y), timeout_after_action=1)
                is_clicked = True
                break
            self.processor.actions.scroll_horizontal(x_axis=400, from_position=HERO_BAR_POSITION)
            sleep(0.5)

        if not is_clicked:
            raise Exception('Did not find hero')

        result = self.processor.image_processing.find_element(MAP_ELEMENT)
        if result.ssim > MAP_ELEMENT.ssim:
            self.processor.actions.click(result, timeout_after_action=2)
