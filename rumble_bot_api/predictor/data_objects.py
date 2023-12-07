from dataclasses import dataclass, field
from rumble_bot_api.desktop_automation_tool.utils.data_objects import Position


@dataclass(kw_only=True)
class PredictionNode:
    top_x: int
    top_y: int
    bottom_x: int
    bottom_y: int
    conf: float
    node_id: int
    name: str = field(init=False)
    center: Position = field(init=False)

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

        self.center = Position(
            x=(self.bottom_x - self.top_x) // 2 + self.top_x,
            y=(self.bottom_y - self.top_y) // 2 + self.top_y
        )
