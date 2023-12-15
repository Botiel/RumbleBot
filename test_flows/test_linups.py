from rumble_bot_api import QuestsMatchObject, PvpMatchObject, MINIS

BARON_PVE = QuestsMatchObject(
    hero=MINIS.baron_rivendare,
    lineup=[
        MINIS.pilot.skill_1,
        MINIS.quilboar.skill_0,
        MINIS.necromancer.skill_1,
        MINIS.prowler.skill_1,
        MINIS.dark_iron_miner.skill_0,
        MINIS.harpies.skill_1,
        MINIS.baron_rivendare.skill_1
    ],
    levelup_list=[]
)

TIRION_PVP = PvpMatchObject(
    hero=MINIS.tirion_fordring,
    lineup=[
        MINIS.darkspear_troll.skill_1,
        MINIS.ghoul.skill_1,
        MINIS.huntress.skill_1,
        MINIS.gryphon_rider.skill_1,
        MINIS.dark_iron_miner.skill_0,
        MINIS.harpies.skill_1,
        MINIS.tirion_fordring.skill_0
    ]
)
