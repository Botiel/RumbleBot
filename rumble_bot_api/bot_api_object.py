from rumble_bot_api.desktop_automation_tool.processors_loader import Processor
from rumble_bot_api.desktop_automation_tool.utils.common import get_yaml_file_path
from rumble_bot_api.bot_core.handlers.quests_handler import QuestsHandler
from rumble_bot_api.bot_core.handlers.pvp_handler import PvpHandler
from rumble_bot_api.bot_core.utils.data_objects import PvpMatchObject, QuestsMatchObject
from rumble_bot_api.bot_core.utils.data_objects import Asset
from typing import Optional


class BaseBotSetup:

    QUESTS_SETUP: Optional[QuestsMatchObject] = None
    PVP_SETUP: Optional[PvpMatchObject] = None

    def __init__(self):
        self._yaml_file = get_yaml_file_path()
        self._processor = Processor(self._yaml_file)
        self._quests_handler = QuestsHandler(self._processor)
        self._pvp_handler = PvpHandler(self._processor)
        self._processor.window.set_window()

        self._setup_quests()
        self._setup_pvp()

        # Commands
        self.wait_for_gold = self._pvp_handler.drop_handler.gold_handler.wait_until_enough_gold
        self.check_gold = self._pvp_handler.drop_handler.gold_handler.get_current_gold_on_bar
        self.get_assets_on_map = self._pvp_handler.drop_handler.predictor.get_assets_on_map
        self.get_current_minis = self._pvp_handler.drop_handler.get_current_minis_on_board
        self.drop_mini = self._pvp_handler.drop_handler.drop_mini
        self.scroll_vertical = self._processor.actions.scroll_vertical
        self.click = self._processor.actions.click

    def _setup_quests(self) -> None:
        if not self.QUESTS_SETUP:
            raise ValueError('Quests match object is not set!')
        self._quests_handler.set_quests_match_object(self.QUESTS_SETUP)

    def _setup_pvp(self) -> None:
        if not self.PVP_SETUP:
            raise ValueError('PvP match object is not set!')

        self.PVP_SETUP.drop_logic = self.pvp_drop_logic
        self.PVP_SETUP.click_arrows_before_match = self.click_arrows_before_match
        self.PVP_SETUP.scroll_up_before_match = self.scroll_up_before_match

        self._pvp_handler.set_pvp_match_object(self.PVP_SETUP)

    def pvp_drop_logic(self) -> None:
        pass

    def click_arrows_before_match(self) -> None:
        pass

    def scroll_up_before_match(self) -> None:
        pass

    @staticmethod
    def check_for_mini(mini: Asset, current: dict) -> tuple:
        minis_list = list(current)
        if mini.name in minis_list:
            return current.get(mini.name)
