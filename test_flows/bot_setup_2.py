from rumble_bot_api import MINIS, BotApi, Position
from rumble_bot_api.bot_core.utils.custom_exceptions import NoMinisOnBoardException


class BotSetup(BotApi):
    # =================== QUESTS =====================
    QUESTS_HERO = MINIS.tirion_fordring
    QUEST_LINEUP = [
        MINIS.darkspear_troll.skill_1,
        MINIS.quilboar.skill_0,
        MINIS.huntress.skill_1,
        MINIS.defias_bandits.skill_0,
        MINIS.dark_iron_miner.skill_0,
        MINIS.harpies.skill_1,
        MINIS.tirion_fordring.skill_0
    ]

    # ==================== PVP =======================
    PVP_HERO = MINIS.tirion_fordring
    PVP_LINEUP = [
        MINIS.darkspear_troll.skill_1,
        MINIS.ghoul.skill_1,
        MINIS.huntress.skill_1,
        MINIS.gryphon_rider.skill_1,
        MINIS.dark_iron_miner.skill_0,
        MINIS.harpies.skill_1,
        MINIS.tirion_fordring.skill_0
    ]

    TOWER_RIGHT = Position(x=620, y=790)
    TOWER_LEFT = Position(x=390, y=790)
    TOP_RIGHT_TOWER = Position(x=790, y=510)

    def click_arrows_before_match(self):
        arrows = self.get_assets_on_map('arrow')
        if arrows:
            return self.click, arrows[0]

    def scroll_up_before_match(self) -> None:
        self.scroll_vertical(220, duration=0.1)

    def get_gold_ores(self) -> tuple:

        upper_top_ore = None
        bottom_top_ore = None
        bottom_ore = None
        gold_positions = self.get_assets_on_map('goldmine')

        if gold_positions:
            for pos in gold_positions:
                if pos.y < 260:
                    upper_top_ore = pos
                elif pos.y > 420:
                    bottom_ore = pos
                else:
                    bottom_top_ore = pos

        return upper_top_ore, bottom_top_ore, bottom_ore

    def drop_miners(self) -> None:

        current = self.get_current_minis()
        dark_miner = self.check_for_mini(MINIS.dark_iron_miner, current)
        miner = self.check_for_mini(MINIS.miner, current)
        upper_top_ore, bottom_top_ore, bottom_ore = self.get_gold_ores()

        if dark_miner:
            if upper_top_ore:
                x = upper_top_ore.x
                y = upper_top_ore.y + 80
                self.drop_mini(dark_miner, Position(x=x, y=y))
            elif bottom_top_ore:
                self.drop_mini(dark_miner, bottom_top_ore)

        if miner:
            if bottom_ore:
                self.drop_mini(miner, self.TOP_RIGHT_TOWER)
            elif (upper_top_ore or bottom_top_ore) and not dark_miner:
                self.drop_mini(miner, self.TOWER_LEFT)

    def pvp_drop_logic(self):

        current_minis = self.get_current_minis()
        if not current_minis:
            raise NoMinisOnBoardException

        order = [
            [MINIS.ghoul, self.TOWER_LEFT],
            [MINIS.darkspear_troll, self.TOWER_LEFT],
            [MINIS.huntress, self.TOP_RIGHT_TOWER],
            [MINIS.tirion_fordring, self.TOWER_RIGHT],
            [MINIS.harpies, self.TOWER_LEFT],
            [MINIS.gryphon_rider, self.TOP_RIGHT_TOWER]
        ]

        for mini, side in order:
            is_mini = self.check_for_mini(mini, current_minis)
            if is_mini:
                self.drop_mini(is_mini, side)
                self.drop_miners()
