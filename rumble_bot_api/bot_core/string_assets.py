from pydantic import BaseModel
from rumble_bot_api.desktop_automation_tool.utils.data_objects import StringElement


class StringAssets(BaseModel):
    RUMBLE: StringElement = StringElement(string='rumble', threshold=200)
    TOOLS: StringElement = StringElement(string='Tools', threshold=180, exact_match=True)
    RUMBLE_PVP: StringElement = StringElement(string='Rumble!', threshold=180, exact_match=True)
    Back_PVP: StringElement = StringElement(string='Back', threshold=180, exact_match=True)
    PVP: StringElement = StringElement(string='pvp', threshold=220)
    CONTINUE: StringElement = StringElement(string='continue')
    PLAY: StringElement = StringElement(string='play', threshold=200)
    CLAIM: StringElement = StringElement(string='claim')
    CLAIM_AFTER_QUEST: StringElement = StringElement(string='Claim!', threshold=230, exact_match=True)
    START: StringElement = StringElement(string='start', threshold=220)
    QUEST: StringElement = StringElement(string='quest!', threshold=210)
    TAP_TO_SKIP: StringElement = StringElement(string='Tap', threshold=100, exact_match=True)
    CLAIM_REWARDS: StringElement = StringElement(string='reward', threshold=230)
    ERROR: StringElement = StringElement(string='Error', threshold=180, exact_match=True)
    FAILED: StringElement = StringElement(string='Failed', threshold=180, exact_match=True)
    LOADING: StringElement = StringElement(string='loading', threshold=200)
    LEVEL_UP: StringElement = StringElement(string='up!', threshold=180)
    TRY_AGAIN: StringElement = StringElement(string='again!', threshold=180)
    OK: StringElement = StringElement(string='OK', threshold=180, exact_match=True)
    VS: StringElement = StringElement(string='vs', threshold=220)
    TROOPS: StringElement = StringElement(string='troops', threshold=180)


STRING_ASSETS = StringAssets()
