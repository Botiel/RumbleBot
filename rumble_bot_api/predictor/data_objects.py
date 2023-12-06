from dataclasses import dataclass, field
from rumble_bot_api.desktop_automation_tool.utils.data_objects import Position


@dataclass(kw_only=True)
class PredictionNode:
    x: int
    y: int
    h: int
    w: int
    conf: float
    node_id: int
    name: str = field(init=False)

    def __post_init__(self):
        match self.node_id:
            case 0:
                self.name = 'goldmine'
            case 1:
                self.name = 'arrow'
            case 2:
                self.name = 'enemy'
            case 3:
                self.name = 'chest'

    def get_pos(self) -> Position:
        return Position(x=self.x, y=self.y)
