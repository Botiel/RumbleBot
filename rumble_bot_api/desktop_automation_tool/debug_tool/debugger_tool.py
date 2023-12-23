import PySimpleGUI as sg
import pyautogui
from rumble_bot_api.desktop_automation_tool.debug_tool.tabs import load_layout
from pathlib import Path
import subprocess
import sys
from rumble_bot_api.desktop_automation_tool.utils.common import get_folder, get_images_as_dict
from rumble_bot_api.desktop_automation_tool.processors_loader import Processor
from rumble_bot_api.desktop_automation_tool.utils.data_objects import Region, Position

ROOT = Path(__file__).resolve().parent.parent.parent
WINDOW_SIZE = (800, 900)
MY_THEME = {'BACKGROUND': '#44475a',
            'TEXT': '#50fa7b',
            'INPUT': '#282a36',
            'TEXT_INPUT': '#50fa7b',
            'SCROLL': '#c7e78b',
            'BUTTON': ('#50fa7b', '#282a36'),
            'PROGRESS': ('#01826B', '#D0D0D0'),
            'BORDER': 2,
            'SLIDER_DEPTH': 0,
            'PROGRESS_DEPTH': 0}

sg.theme_add_new('nuri', MY_THEME)
sg.theme('nuri')


class DebuggerTool:

    def __init__(self, yaml_file: str | Path, title: str = 'Debugger', custom_functions: dict = None):
        self.processors = Processor(yaml_file)
        self.images_dict = get_images_as_dict()
        self.custom_functions = custom_functions

        layout = load_layout(
            yaml_config=self.processors.yaml_config,
            images_dict=self.images_dict,
            custom_functions=custom_functions
        )

        self.processors.image_processing.set_save_image_on()
        self.processors.tesseract.set_save_image_on()
        self.window = sg.Window(title, layout=layout, size=WINDOW_SIZE, finalize=True)

    def get_coordinates_and_color(self) -> None:

        try:
            window_x = self.processors.window.window.topleft.x
            window_y = self.processors.window.window.topleft.y
            x, y = pyautogui.position()
            self.window['-COORDINATES-'].update(f'({x - window_x}, {y - window_y})')
        except Exception as e:
            self.window['-COORDINATES-'].update('Emulator Not Found!')
            return

        try:
            pixel_color = pyautogui.pixel(x, y)
            hex_color = '#{:02x}{:02x}{:02x}'.format(pixel_color[0], pixel_color[1], pixel_color[2])
            self.window['-COLOR-'].update(hex_color)
        except Exception as e:
            print(f"Error: {e}")

    def events(self) -> None:
        event, values = self.window.read(timeout=100)

        if self.custom_functions:
            for button, func in self.custom_functions['buttons'].items():
                if event == button:
                    func(self.window, self.processors)

        if event == sg.WIN_CLOSED:
            sys.exit(0)

        if event == 'SET_WINDOW_BTN':
            self.processors.window.set_window()

        if event == 'TAKE_SCREENSHOT_BTN':
            self.processors.window.get_window_screenshot(save_image=True, generate_name=True)

        if event == 'EXTRACT_STRINGS_BTN':
            self.window['DISPLAY'].update('')
            text = self.processors.tesseract.extract_strings_from_window_image(
                threshold=int(self.window['STRING_THRESHOLD'].get()),
                only_text=True
            )
            for t in text:
                if t:
                    print(t)

        if event == 'GET_XY_BTN':
            self.window['DISPLAY'].update('')
            results = self.processors.tesseract.extract_string_coordinates_from_tesseract_data(
                string=self.window['STRING_INPUT'].get(),
                threshold=int(self.window['COORDINATES_THRESHOLD'].get()),
                exact_match=self.window['EXACT_MATCH'].get(),
            )
            for res in results:
                print(res)

        if event == 'CHECK_XY':
            self.processors.window.move_to(
                x=int(self.window['X_VALUE'].get()),
                y=int(self.window['Y_VALUE'].get())
            )

        if event == 'FIND_IMAGE_BTN':
            self.window['DISPLAY'].update('')
            name = self.window['IMAGE_NAME'].get()
            path = self.images_dict.get(name)

            try:
                x_top = int(self.window['REGION_TOP_LEFT_X'].get())
                y_top = int(self.window['REGION_TOP_LEFT_Y'].get())
                x_bottom = int(self.window['REGION_BOTTOM_RIGHT_X'].get())
                y_bottom = int(self.window['REGION_BOTTOM_RIGHT_Y'].get())
            except Exception:
                region = None
            else:
                region = Region(
                    top_left=Position(x=x_top, y=y_top),
                    bottom_right=Position(x=x_bottom, y=y_bottom)
                )

            if path:
                threshold = self.window['IMAGE_THRESHOLD'].get()
                result = self.processors.image_processing.find_object_on_screen_get_coordinates(
                    image_path=path,
                    threshold=int(threshold) if threshold else None,
                    specific_region=region
                )
                print('x: ', result[0])
                print('y: ', result[1])
                print('similarity score [0-1]: ', result[2])

            else:
                print('No such element image')

        if event == 'SHOW_IMAGES':
            output = get_folder(self.processors.yaml_config, 'output')
            subprocess.Popen(['explorer', str(output)])

        self.get_coordinates_and_color()

    def main_loop(self):

        while True:
            try:
                self.events()
            except Exception as e:
                print(e)
