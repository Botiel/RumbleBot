import PySimpleGUI as sg

TEXT_SIZE = (15, 1)
INPUT_SIZE = (30, 1)
FOCUS_TEXT = (3, 1)
FOCUS_INPUT = (20, 1)
DROP_TEXT = (16, 1)
DROP_INPUT = (5, 1)


def load_layout(yaml_config: dict, images_dict: dict, custom_functions: dict = None) -> list:
    coordinates_frame = [
        [sg.Text("")],

        [
            sg.Text('Mouse Coordinates:', size=(15, 1)),
            sg.Text('', size=(50, 1), key='-COORDINATES-')
        ],

        [sg.Text('Pixel Color (Hex):', size=(15, 1)), sg.Text('', size=(10, 1), key='-COLOR-')],

        [sg.Text("")],
    ]

    general_config = [
        [sg.Text("")],

        [sg.Text("Tesseract Path:", size=TEXT_SIZE),
         sg.InputText(size=(60, 1), key="TESSERACT_PATH", default_text=yaml_config.get('tesseract_path'))],

        [sg.Text("Emulator Path:", size=TEXT_SIZE),
         sg.InputText(size=(60, 1), key="EMULATOR_PATH", default_text=yaml_config.get('window_path'))],

        [sg.Text("Window Title:", size=TEXT_SIZE),
         sg.InputText(size=(60, 1), key="EMULATOR_TITLE", default_text=yaml_config.get('window_title'))],

        [sg.Text("")],

        [sg.Button("Set Window", pad=10, size=10, key="SET_WINDOW_BTN")]

    ]

    tesseract = [
        [sg.Text("")],

        [
            sg.Button("Extract Text", pad=10, size=10, key="EXTRACT_STRINGS_BTN"),
            sg.Text("Threshold:", size=(7, 1)), sg.InputText(size=(5, 1), key="STRING_THRESHOLD", default_text='180')
        ],

        [
            sg.Button("Get Element", pad=10, size=10, key="GET_XY_BTN"), sg.Text("String:", size=(5, 1)),
            sg.InputText(size=(7, 1), key="STRING_INPUT", default_text=''), sg.Text("Threshold:", size=(7, 1)),
            sg.InputText(size=(5, 1), key="COORDINATES_THRESHOLD", default_text='180'),
            sg.Checkbox('Exact Match', key='EXACT_MATCH', default=False)
        ],

    ]

    image = [

        [
            sg.Text("Image Name:", size=(15, 1)),
            sg.DropDown(
                size=(15, 1),
                key="IMAGE_NAME",
                default_value='',
                values=list(images_dict)
            )
        ],

        [sg.Text("Image Threshold:", size=(15, 1)), sg.InputText(size=(7, 1), key="IMAGE_THRESHOLD", default_text='')],

        [
            sg.Text("Region:", size=(15, 1)),
            sg.Text("top_left_xy", size=(8, 1)),
            sg.InputText(size=(5, 1), key="REGION_TOP_LEFT_X"),
            sg.InputText(size=(5, 1), key="REGION_TOP_LEFT_Y"),

            sg.Text("bottom_right_xy", size=(12, 1)),
            sg.InputText(size=(5, 1), key="REGION_BOTTOM_RIGHT_X"),
            sg.InputText(size=(5, 1), key="REGION_BOTTOM_RIGHT_Y"),
        ],

        [sg.Button("Find Image", pad=10, size=10, key="FIND_IMAGE_BTN")],

    ]

    functions_tab = custom_functions.get('layout') if custom_functions else []
    tabs = [
        sg.TabGroup([[
            sg.Tab("Tesseract", tesseract),
            sg.Tab("Image Processing", image),
            sg.Tab("Functions", functions_tab)

        ]], size=(800, 170))
    ]

    layout = [
        [sg.Frame(title="General Config", layout=general_config, border_width=1, size=(800, 200))],

        [sg.Text("")],

        [sg.Frame(title="Coordinates & Colors", layout=coordinates_frame, border_width=1, size=(800, 120))],

        [sg.Text("")],

        [tabs],

        [
            sg.Button("Show Images", pad=10, size=10, key="SHOW_IMAGES"),
            sg.Button("Check XY", pad=10, size=10, key="CHECK_XY"),
            sg.Text("x:", size=(2, 1)), sg.InputText(size=(5, 1), key="X_VALUE", default_text='0'),
            sg.Text("y:", size=(2, 1)), sg.InputText(size=(5, 1), key="Y_VALUE", default_text='0'),
        ],

        [[sg.Output(size=(115, 50), key="DISPLAY")]]

    ]

    return layout
