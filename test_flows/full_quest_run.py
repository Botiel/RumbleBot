from rumble_bot_api.bot_core.handlers.quests_handler import QuestsHandler
from rumble_bot_api.bot_core.mini_assets import MINI_ASSETS
from test_flows.utils import init_processor


if __name__ == '__main__':

    lineup = [
        MINI_ASSETS.prowler.skill_1,
        MINI_ASSETS.necromancer.skill_1,
        MINI_ASSETS.gryphon_rider.skill_1,
        MINI_ASSETS.pilot.no_skill,
        MINI_ASSETS.harpies.skill_1,
        MINI_ASSETS.ghoul.skill_1,
        MINI_ASSETS.baron_rivendare.skill_1

    ]
    levelup = [MINI_ASSETS.pilot.name]

    p = init_processor()
    q = QuestsHandler(p, lineup, levelup)

    q.main_loop()
