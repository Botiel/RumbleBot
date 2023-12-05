from rumble_bot_api.bot_core.handlers.quests_handler import QuestsHandler
from rumble_bot_api.bot_core.mini_assets import MINI_ASSETS
from test_flows.utils import init_processor


if __name__ == '__main__':

    lineup = [
        MINI_ASSETS.stonehoof_tauren.no_skill,
        MINI_ASSETS.ghoul.no_skill,
        MINI_ASSETS.necromancer.no_skill,
        MINI_ASSETS.gryphon_rider.no_skill,
        MINI_ASSETS.pilot.no_skill,
        MINI_ASSETS.harpies.no_skill,
        MINI_ASSETS.baron_rivendare.no_skill

    ]
    levelup = [MINI_ASSETS.pilot.name]

    p = init_processor()
    q = QuestsHandler(p, lineup, levelup)

    q.main_loop()
