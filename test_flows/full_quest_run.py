from rumble_bot_api.bot_core.handlers.quests_handler import QuestsHandler
from rumble_bot_api.bot_core.mini_assets import MINI_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import MatchLineup
from test_flows.utils import init_processor


if __name__ == '__main__':

    match_lineup = MatchLineup(
        hero=MINI_ASSETS.baron_rivendare,
        lineup=[
            MINI_ASSETS.prowler.skill_1,
            MINI_ASSETS.necromancer.skill_1,
            MINI_ASSETS.gryphon_rider.skill_1,
            MINI_ASSETS.pilot.no_skill,
            MINI_ASSETS.harpies.skill_1,
            MINI_ASSETS.ghoul.skill_1,
            MINI_ASSETS.baron_rivendare.skill_1
        ],
        levelup_list=[MINI_ASSETS.pilot]
    )

    p = init_processor()
    q = QuestsHandler(p, match_lineup)

    q.main_loop()
