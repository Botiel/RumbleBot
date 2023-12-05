from pathlib import Path
from rumble_bot_api.desktop_automation_tool.processors_loader import Processor
from rumble_bot_api.bot_core.utils.common import set_logger

ROOT = Path(__file__).resolve().parent.parent
YAML_FILE = ROOT / 'config.yaml'


def init_processor() -> Processor:
    set_logger(20)
    p = Processor(YAML_FILE)
    p.window.set_window()
    return p
