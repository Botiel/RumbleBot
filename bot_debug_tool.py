from desktop_automation_tool.debug_tool.debugger_tool import DebuggerTool
from desktop_automation_tool.processors_loader import Processor
from predictor.predictor_object import Predictor
from bot_api.handlers.gold_handler import GoldHandler
from pathlib import Path
import PySimpleGUI as sg

ROOT = Path(__file__).resolve().parent
MODELS = ROOT / 'predictor' / 'models'


def make_prediction(gui_window: sg.Window, processor: Processor) -> None:
    gui_window['DISPLAY'].update('')
    model_option = gui_window['MODEL_OPTIONS'].get()
    conf = gui_window['CONFIDENCE'].get()

    try:
        f_conf = float(conf)
    except Exception as e:
        print(e)
        print('Using default conf for goldmine model')
        f_conf = None

    p = Predictor(processor.window)
    res = p.predict(model_name=model_option, return_type='positions', save=True, conf=f_conf)
    print(res)


def get_gold(gui_window: sg.Window, processor: Processor) -> None:
    gui_window['DISPLAY'].update('')
    gold_handler = GoldHandler(processor)
    curr_gold = gold_handler.get_current_gold_on_bar()
    print(curr_gold)


EXTRA_LAYOUT = [
    [sg.Text("")],

    [
        sg.Button('Predict', pad=10, size=10, key='PREDICT_BTN'),
        sg.Text('Model:', size=(7, 1)),
        sg.DropDown(size=(15, 1), key='MODEL_OPTIONS', values=[item.name.split('.')[0] for item in MODELS.iterdir()]),
        sg.Text('Confidence:', size=(10, 1)),
        sg.InputText(size=(6, 1), key="CONFIDENCE")
    ],

    [sg.Text("")],

    [sg.Button('Get Gold', pad=10, size=10, key='GET_GOLD_BTN')]
]


CUSTOM_FUNCTIONS = {
    'layout': EXTRA_LAYOUT,
    'buttons': {
        'PREDICT_BTN': make_prediction,
        'GET_GOLD_BTN': get_gold
    }
}


def main() -> None:
    tool = DebuggerTool(yaml_file='config.yaml', custom_functions=CUSTOM_FUNCTIONS)
    tool.main_loop()


if __name__ == '__main__':
    main()
