from rumble_bot_api.bot_core.utils.data_objects import create_asset, Asset
from rumble_bot_api.desktop_automation_tool import Region, Position
from pydantic import BaseModel


class MiniAssets(BaseModel):
    ssim: float = 0.7
    region: Region = Region(top_left=Position(x=330, y=830), bottom_right=Position(x=770, y=970))

    # Minis
    baron_rivendare: Asset = create_asset(name='baron_rivendare', cost=4)
    bat_rider: Asset = create_asset(name='bat_rider', cost=2)
    cairne_bloodhoof: Asset = create_asset('cairne_bloodhoof', cost=5)
    flamewaker: Asset = create_asset('flamewaker', cost=4)
    ghoul: Asset = create_asset('ghoul', cost=2)
    gryphon_rider: Asset = create_asset('gryphon_rider', cost=2)
    harpies: Asset = create_asset('harpies', cost=3)
    miner: Asset = create_asset('miner', cost=1)
    necromancer: Asset = create_asset('necromancer', cost=4)
    pilot: Asset = create_asset('pilot', cost=3, is_unbound=True)
    prowler: Asset = create_asset('prowler', cost=3)
    pyromancer: Asset = create_asset('pyromancer', cost=3)
    sylvanas_windrunner: Asset = create_asset('sylvanas_windrunner', cost=6)
    stonehoof_tauren: Asset = create_asset('stonehoof_tauren', cost=4)
    darkspear_troll: Asset = create_asset('darkspear_troll', cost=3)
    quilboar: Asset = create_asset('quilboar', cost=2, is_unbound=True)
    tirion_fordring: Asset = create_asset('tirion_fordring', cost=4)
    huntress: Asset = create_asset('huntress', cost=5)
    dark_iron_miner: Asset = create_asset('dark_iron_miner', cost=2, is_unbound=True)
    footmen: Asset = create_asset('footmen', cost=5)
    defias_bandits: Asset = create_asset('defias_bandits', cost=1)
    hogger: Asset = create_asset('hogger', cost=4)
    murloc_tidehunters: Asset = create_asset('murloc_tidehunters', cost=2)


MINI_ASSETS = MiniAssets()
