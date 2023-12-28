from pprint import pprint
from pydantic import BaseModel, Field
from enum import Enum
from typing import Callable
from rumble_bot_api.bot_core.utils.common import MINIS_FOLDER


class GameState(Enum):
    ERROR_STATE = 'error_state'
    INIT_QUESTS = 'init_quests'
    QUESTS_MATCH_LOOP = 'quests_match_loop'
    QUESTS_GAME_FINISH = 'quests_game_finish'
    INIT_PVP = 'init_pvp'
    PVP_MATCH_LOOP = 'pvp_match_loop'
    PVP_GAME_FINISH = 'pvp_game_finish'
    INIT_BOSS = 'init_boss'
    PRE_BOSS_MATCH = 'pre_boss_match'
    BOSS_MATCH_LOOP = 'boss_match_loop'
    BOSS_GAME_FINISH = 'boss_game_finish'


class Node(BaseModel):
    name: str = Field(default=None)
    path: str = Field(default=None)
    cost: int = Field(default=None)


class Asset(BaseModel):
    name: str = Field(default=None)
    is_unbound: bool = Field(default=False)
    is_spell: bool = Field(default=False)
    skill_0: Node = Field(default=None)
    skill_1: Node = Field(default=None)
    skill_2: Node = Field(default=None)
    skill_3: Node = Field(default=None)


class MatchObject(BaseModel):
    lineup: list[Node]
    hero: Asset
    levelup_list: list[Asset] = []


class PvpMatchObject(BaseModel):
    lineup: list[Node]
    hero: Asset
    drop_logic: Callable = None
    click_arrows_before_match: Callable = None
    scroll_up_before_match: Callable = None


def create_asset(
        name: str,
        cost: int,
        is_unbound: bool = False,
        is_spell: bool = False,
        changed_cost: dict = None
) -> Asset:
    temp = {
        'name': name,
        'is_unbound': is_unbound,
        'is_spell': is_spell,
        'skill_0': {
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
