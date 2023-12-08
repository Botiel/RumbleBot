from rumble_bot_api.desktop_automation_tool.debug_tool.debugger_tool import DebuggerTool
from rumble_bot_api.desktop_automation_tool.processors_loader import Processor
from rumble_bot_api.predictor.predictor_object import Predictor
from rumble_bot_api.bot_core.handlers.gold_handler import GoldHandler
from dataclasses import asdict
from pathlib import Path
import PySimpleGUI as sg
import shutil

ROOT = Path(__file__).resolve().parent
MODELS = ROOT / 'predictor' / 'models'


def find_root_dir() -> Path:
    current_path = Path.cwd().resolve()
    src = current_path / 'desktop_automation_tool' / 'extra' / 'config.yaml'

    while True:
        curr = current_path / 'venv'
        if curr.exists() and current_path.is_dir():
            dst = current_path / 'config.yaml'
            if not dst.exists():
                shutil.copy(src=src, dst=dst)
            return current_path

        if curr.name.lower() == 'users':
            raise Exception('Could not find project root, please create a venv')

        current_path = current_path.parent


def make_prediction(gui_window: sg.Window, processor: Processor) -> None:
    gui_window['DISPLAY'].update('')
    conf = gui_window['CONFIDENCE'].get()

    try:
        f_conf = float(conf)
    except Exception:
        f_conf = 0.8

    p = Predictor(processor.window, processor.yaml_config)
    res = p.predict(save=True, conf=f_conf)
    res_as_dict = asdict(res)

    for k, v in res_as_dict.items():
        for item in v:
            print(f"[{item['name']}] [{item['center']['x']}, {item['center']['y']}]\n")


def get_gold(gui_window: sg.Window, processor: Processor) -> None:
    gui_window['DISPLAY'].update('')
    gold_handler = GoldHandler(processor)
    curr_gold = gold_handler.get_current_gold_on_bar()
    print(curr_gold)


def get_extra_layout() -> list:
    return [
        [sg.Text("")],

        [
            sg.Button('Predict', pad=10, size=10, key='PREDICT_BTN'),
            sg.Text('Confidence:', size=(10, 1)),
            sg.InputText(size=(6, 1), key="CONFIDENCE")
        ],

        [sg.Text("")],

        [sg.Button('Get Gold', pad=10, size=10, key='GET_GOLD_BTN')]
    ]


def main() -> None:
    custom_functions = {
        'layout': get_extra_layout(),
        'buttons': {
            'PREDICT_BTN': make_prediction,
            'GET_GOLD_BTN': get_gold
        }
    }
    project_dir = find_root_dir()
    yaml_file = project_dir / 'config.yaml'

    tool = DebuggerTool(yaml_file=yaml_file, custom_functions=custom_functions)
    tool.main_loop()


if __name__ == '__main__':
    main()
