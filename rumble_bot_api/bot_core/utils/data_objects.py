from pprint import pprint
from pydantic import BaseModel, Field
from rumble_bot_api.bot_core.utils.common import MINIS_FOLDER


class Node(BaseModel):
    name: str = Field(default=None)
    path: str = Field(default=None)
    cost: int = Field(default=None)


class Asset(BaseModel):
    name: str = Field(default=None)
    no_skill: Node = Field(default=None)
    skill_1: Node = Field(default=None)
    skill_2: Node = Field(default=None)
    skill_3: Node = Field(default=None)


def create_asset(name: str, cost: int, changed_cost: dict = None) -> Asset:
    temp = {
        'name': name,
        'no_skill': {
            'path': str(MINIS_FOLDER / f'{name}_0.png'),
            'cost': cost,
            'name': name
        },
        'skill_1': {
            'path': str(MINIS_FOLDER / f'{name}_1.png'),
            'cost': cost,
            'name': name
        },
        'skill_2': {
            'path': str(MINIS_FOLDER / f'{name}_2.png'),
            'cost': cost,
            'name': name
        },
        'skill_3': {
            'path': str(MINIS_FOLDER / f'{name}_3.png'),
            'cost': cost,
            'name': name
        }
    }

    if changed_cost:
        for k, v in temp.items():
            for _skill, _cost in changed_cost.items():
                if k == _skill:
                    temp[_skill]['cost'] = _cost

    return Asset(**temp)


if __name__ == '__main__':
    x = create_asset('baron_rivendare', cost=4, changed_cost={'skill_2': 7})
    pprint(x.model_dump())
