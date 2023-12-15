from rumble_bot_api.bot_core.handlers.quests_handler import QuestsHandler
from rumble_bot_api.bot_core.mini_assets import MINI_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import MatchObject
from test_flows.utils import init_processor


if __name__ == '__main__':

    match_setup = MatchObject(
        hero=MINI_ASSETS.baron_rivendare,
        lineup=[
            MINI_ASSETS.prowler.skill_1,
            MINI_ASSETS.necromancer.skill_1,
            MINI_ASSETS.harpies.skill_1,
            MINI_ASSETS.gryphon_rider.skill_1,
            MINI_ASSETS.pilot.skill_1,
            MINI_ASSETS.ghoul.skill_1,
            MINI_ASSETS.baron_rivendare.skill_1
        ],
        levelup_list=[]
    )

    p = init_processor()
    q = QuestsHandler(p)
    q.set_match_object(match_setup)

    q.main_loop()
