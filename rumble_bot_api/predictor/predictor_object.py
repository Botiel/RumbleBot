import cv2
import os
import numpy as np
from pathlib import Path
from typing import Literal
from time import perf_counter
from ultralytics import YOLO
from ultralytics.engine.results import Results
from rumble_bot_api.predictor.data_objects import PredictionNode, PredictionCluster
from rumble_bot_api.desktop_automation_tool.processors.window_object import WindowObject
from rumble_bot_api.desktop_automation_tool.utils.data_objects import Position
from rumble_bot_api.desktop_automation_tool.utils.common import get_output_folder


CURR = Path(__file__).resolve().parent
MODEL_PATH = CURR / 'rumble.pt'


class Predictor:

    def __init__(self, window: WindowObject, model_path: str = str(MODEL_PATH)):
        self.window = window
        self._output_dir = get_output_folder()
        self.model_path = model_path

        if not os.path.exists(self._output_dir):
            os.makedirs(self._output_dir, exist_ok=True)

    def predict(self, image: str | np.ndarray = None, conf: float = 0.8, save: bool = False) -> PredictionCluster:

        start = perf_counter()

        if isinstance(image, str):
            image = cv2.imread(image)

        if image is None:
            image = self.window.get_window_screenshot()

        model = YOLO(self.model_path)

        results: Results = model.predict(
            source=image,
            conf=conf,
            save=save,
            device=0,
            project=self._output_dir
        )

        prediction_cluster = PredictionCluster()
        for result in results:
            for node in result.boxes.data.tolist():
                temp_node = PredictionNode(
                    top_x=int(node[0]),
                    top_y=int(node[1]),
                    bottom_x=int(node[2]),
                    bottom_y=int(node[3]),
                    conf=node[4],
                    node_id=int(node[5]),
                )
                match temp_node.name:
                    case 'goldmine':
                        prediction_cluster.goldmine.append(temp_node)
                    case 'arrow':
                        prediction_cluster.arrow.append(temp_node)
                    case 'enemy':
                        prediction_cluster.enemy.append(temp_node)
                    case 'chest':
                        prediction_cluster.chest.append(temp_node)

        end = perf_counter()
        delta = end - start
        print(f"Detection time: {delta:.4f} seconds")

        return prediction_cluster

    def get_assets_on_map(self, asset: Literal['goldmine', 'arrow', 'enemy', 'chest']) -> list[Position] | None:
        cluster = self.predict()
        assets = cluster.get_prediction_asset(asset)
        if assets:
            return [obj.center for obj in assets]
