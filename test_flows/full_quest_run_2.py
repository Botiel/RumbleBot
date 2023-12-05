from rumble_bot_api.bot_core.handlers.quests_handler import QuestsHandler
from rumble_bot_api.bot_core.handlers.hero_manager_handler import HeroManagerHandler
from rumble_bot_api.bot_core.mini_assets import MINI_ASSETS
from rumble_bot_api.bot_core.utils.data_objects import MatchLineup
from test_flows.utils import init_processor


if __name__ == '__main__':

    match_lineup = MatchLineup(
        hero=MINI_ASSETS.baron_rivendare,
        lineup=[
            MINI_ASSETS.stonehoof_tauren.no_skill,
            MINI_ASSETS.ghoul.no_skill,
            MINI_ASSETS.necromancer.no_skill,
            MINI_ASSETS.gryphon_rider.no_skill,
            MINI_ASSETS.pilot.no_skill,
            MINI_ASSETS.harpies.no_skill,
            MINI_ASSETS.baron_rivendare.no_skill
        ],
        levelup_list=[MINI_ASSETS.pilot]
    )

    p = init_processor()
    m = HeroManagerHandler(p)
    m.switch_hero(MINI_ASSETS.baron_rivendare.name)
    q = QuestsHandler(p, match_lineup)

    q.main_loop()
