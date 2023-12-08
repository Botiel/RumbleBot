from ultralytics import YOLO
from ultralytics.engine.results import Results
import numpy as np
import cv2
import os
from pathlib import Path
from rumble_bot_api.predictor.data_objects import PredictionNode, PredictionCluster
from rumble_bot_api.desktop_automation_tool.processors.window_object import WindowObject


CURR = Path(__file__).resolve().parent
MODEL_PATH = CURR / 'rumble.pt'


class Predictor:

    def __init__(self, window: WindowObject, yaml_config: dict, model_path: str = str(MODEL_PATH)):
        self.window = window
        self.output_dir = f"{yaml_config.get('project_root')}/output"
        self.model_path = model_path

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)

    def predict(self, image: str | np.ndarray = None, conf: float = 0.8, save: bool = False) -> PredictionCluster:

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

        return prediction_cluster
