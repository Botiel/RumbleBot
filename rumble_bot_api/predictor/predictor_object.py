from ultralytics import YOLO
from ultralytics.engine.results import Results
import numpy as np
import cv2
import os
from typing import Literal
from pathlib import Path
from rumble_bot_api.predictor.data_objects import PredictionNode
from rumble_bot_api.desktop_automation_tool.processors.window_object import WindowObject


CURR = Path(__file__).resolve().parent
MODEL_PATH = CURR / 'rumble.pt'
PredictionType = Literal['goldmine', 'arrow', 'enemy', 'chest', 'all']


class Predictor:

    NODES_MAP = {
        'goldmine': 0,
        'arrow': 1,
        'enemy': 2,
        'chest': 3
    }

    def __init__(self, window: WindowObject, yaml_config: dict, model_path: str = str(MODEL_PATH)):
        self.window = window
        self.output_dir = f"{yaml_config.get('project_root')}/output"
        self.model_path = model_path

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def predict(
            self,
            prediction_type: PredictionType,
            image: str | np.ndarray = None,
            conf: float = 0.8,
            save: bool = False
    ) -> list[PredictionNode]:

        if isinstance(image, str):
            image = cv2.imread(image)

        if image is None:
            image = self.window.get_window_screenshot()

        model = YOLO(self.model_path)

        results: Results = model.predict(
            source=image,
            conf=conf,
            save=save,
            project=self.output_dir
        )

        prediction_li = []
        for result in results:
            for node in result.boxes.data.tolist():
                if int(node[-1]) == self.NODES_MAP.get(prediction_type) or prediction_type == 'all':
                    prediction_li.append(
                        PredictionNode(
                            x=int(node[0]),
                            y=int(node[1]),
                            h=int(node[2]),
                            w=int(node[3]),
                            conf=node[4],
                            node_id=int(node[5]),
                        )
                    )

        return prediction_li
