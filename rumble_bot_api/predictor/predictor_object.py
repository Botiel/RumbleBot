from ultralytics import YOLO
from ultralytics.engine.results import Results
import numpy as np
import cv2
import os
from torch import Tensor
from pathlib import Path
from typing import Literal
from dataclasses import dataclass
from rumble_bot_api.desktop_automation_tool.utils.data_objects import Position
from rumble_bot_api.desktop_automation_tool.processors.window_object import WindowObject


@dataclass(kw_only=True)
class Model:
    path: str
    conf: float


CURR = Path(__file__).resolve().parent
MODELS_FOLDER = CURR / 'models'


class Predictor:

    MODELS_DICT = {
        'gold': Model(path=str(MODELS_FOLDER / 'gold.pt'), conf=0.9),
        'arrow': Model(path=str(MODELS_FOLDER / 'arrow.pt'), conf=0.85)
    }

    def __init__(self, window: WindowObject, yaml_config: dict):
        self.window = window
        self.output_dir = f"{yaml_config.get('project_root')}/output"

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def predict(
            self,
            model_name: Literal['gold', 'enemy', 'arrow'],
            return_type: Literal['positions', 'tensor'] = 'positions',
            image: str | np.ndarray = None,
            conf: float = None,
            save: bool = False
    ) -> Tensor | list[Position]:

        if isinstance(image, str):
            image = cv2.imread(image)

        if image is None:
            image = self.window.get_window_screenshot()

        model_obj = self.MODELS_DICT.get(model_name)
        if model_obj is None:
            raise ValueError(f'No such model: {model_name}')

        model = YOLO(model_obj.path)
        results: Results = model.predict(
            source=image,
            conf=conf if conf else model_obj.conf,
            save=save,
            project=self.output_dir
        )
        
        tensor = Tensor()
        for r in results:
            tensor = r.boxes.xywh

        if return_type == 'tensor':
            return tensor
        elif return_type == 'positions':
            return [Position(x=int(t[0]), y=int(t[1])) for t in tensor]
        else:
            raise ValueError(f'No such return type: {return_type}')



