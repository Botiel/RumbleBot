from rumble_bot_api import MINIS, BotApi, Position
from random import choice


class BotSetup(BotApi):

    # =================== QUESTS =====================
    QUESTS_HERO = MINIS.baron_rivendare
    QUESTS_MINI_1 = MINIS.darkspear_troll.skill_0
    QUESTS_MINI_2 = MINIS.ghoul.skill_0
    QUESTS_MINI_3 = MINIS.necromancer.skill_0
    QUESTS_MINI_4 = MINIS.gryphon_rider.skill_0
    QUESTS_MINI_5 = MINIS.pilot.skill_0
    QUESTS_MINI_6 = MINIS.harpies.skill_0
    QUESTS_MINI_7 = MINIS.baron_rivendare.skill_0

    LEVELUP_LIST = [
        MINIS.pilot,
        MINIS.ghoul
    ]

    # ==================== PVP =======================
    PVP_HERO = MINIS.baron_rivendare
    PVP_MINI_1 = MINIS.darkspear_troll.skill_0
    PVP_MINI_2 = MINIS.ghoul.skill_0
    PVP_MINI_3 = MINIS.necromancer.skill_0
    PVP_MINI_4 = MINIS.gryphon_rider.skill_0
    PVP_MINI_5 = MINIS.pilot.skill_0
    PVP_MINI_6 = MINIS.harpies.skill_0
    PVP_MINI_7 = MINIS.baron_rivendare.skill_0

    def pvp_before_match_logic(self):
        arrows = self.get_assets_on_map('arrow')
        if arrows:
            return self.click, arrows[0]

    def pvp_match_logic(self):

        tower_right = Position(x=660, y=480)
        tower_left = Position(x=360, y=480)
        top_right_tower = Position(x=723, y=294)

        current_minis = self.get_current_minis()

        for mini_name, mini_position_and_cost in current_minis.items():

            if mini_name == MINIS.ghoul.name:
                dropzone = top_right_tower

            elif mini_name == MINIS.harpies.name:
                dropzone = tower_left

            elif mini_name == MINIS.necro.name:
                dropzone = tower_right

            elif mini_name == MINIS.gryph.name:
                dropzone = tower_left

            elif mini_name == MINIS.troll.name:
                dropzone = tower_right

            elif mini_name == MINIS.baron.name:
                dropzone = tower_left

            elif mini_name == MINIS.pilot.name:
                dropzone = top_right_tower

            else:
                continue

            self.drop_mini(mini_position_and_cost, dropzone)

            if 'miner' in list(current_minis):

                gold_positions = self.get_assets_on_map('goldmine')

                if not gold_positions:
                    continue

                if len(gold_positions) > 1:
                    side = choice(gold_positions)
                else:
                    side = gold_positions[0]

                miner = current_minis.get('miner')
                dropzone = tower_left if side.x < 500 else tower_right
                self.drop_mini(miner, dropzone)
