from dataclasses import dataclass, field


@dataclass(kw_only=True)
class Position:
    x: int
    y: int


@dataclass(kw_only=True)
class Region:
    top_left: Position
    bottom_right: Position

    def get_full_region(self) -> list[tuple]:
        return [
            (self.top_left.x, self.top_left.y),
            (self.bottom_right.x, self.top_left.y),
            (self.bottom_right.x, self.bottom_right.y),
            (self.top_left.x, self.bottom_right.y)
        ]


@dataclass(kw_only=True)
class StringElement:
    string: str
    threshold: int = 170
    exact_match: bool = False
    region: Region | None = None


@dataclass(kw_only=True)
class ImageElement:
    name: str
    path: str
    threshold: int = 0
    region: Region | None = None
    ssim: float | None = None


@dataclass(kw_only=True)
class Rect:
    x: int
    y: int
    width: int
    height: int
    string: str
    center: Position = field(init=False)

    def __post_init__(self):
        self.center = Position(
            x=self.x + self.width // 2,
            y=self.y + self.height // 2
        )


@dataclass(kw_only=True)
class ImagePosition:
    x: int
    y: int
    ssim: float
