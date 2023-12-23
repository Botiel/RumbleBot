from rumble_bot_api import QuestsMatchObject, PvpMatchObject, MINIS

BARON_PVE = QuestsMatchObject(
    hero=MINIS.baron_rivendare,
    lineup=[
        MINIS.huntress.skill_1,
        MINIS.ghoul.skill_1,
        MINIS.necromancer.skill_1,
        MINIS.darkspear_troll.skill_1,
        MINIS.dark_iron_miner.skill_0,
        MINIS.harpies.skill_1,
        MINIS.baron_rivendare.skill_1
    ],
    levelup_list=[
        MINIS.quilboar,
        MINIS.footmen,
        MINIS.pilot,
        MINIS.darkspear_troll,
        MINIS.sylvanas_windrunner,
    ]
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

TIRION_PVE = QuestsMatchObject(
    hero=MINIS.tirion_fordring,
    lineup=[
        MINIS.footmen.skill_0,
        MINIS.darkspear_troll.skill_1,
        MINIS.pilot.skill_1,
        MINIS.quilboar.skill_0,
        MINIS.dark_iron_miner.skill_0,
        MINIS.harpies.skill_1,
        MINIS.tirion_fordring.skill_0
    ],
    levelup_list=[
        MINIS.quilboar,
        MINIS.footmen,
        MINIS.pilot,
        MINIS.darkspear_troll,
        MINIS.tirion_fordring,
    ]
)

HOGGER_PVP = PvpMatchObject(
    hero=MINIS.hogger,
    lineup=[
        MINIS.hogger.skill_0,
        MINIS.darkspear_troll.skill_1,
        MINIS.gryphon_rider.skill_1,
        MINIS.prowler.skill_1,
        MINIS.murloc_tidehunters.skill_1,
        MINIS.quilboar.skill_0,
        MINIS.dark_iron_miner.skill_0,
    ]
)

BARON_PVP = PvpMatchObject(
    hero=MINIS.baron_rivendare,
    lineup=[
        MINIS.necromancer.skill_1,
        MINIS.darkspear_troll.skill_1,
        MINIS.harpies.skill_1,
        MINIS.huntress.skill_1,
        MINIS.baron_rivendare.skill_1,
        MINIS.ghoul.skill_1,
        MINIS.dark_iron_miner.skill_0,
    ]
)

SYLVANA_PVE = QuestsMatchObject(
    hero=MINIS.sylvanas_windrunner,
    lineup=[
        MINIS.ghoul.skill_1,
        MINIS.sylvanas_windrunner.skill_1,
        MINIS.darkspear_troll.skill_1,
        MINIS.necromancer.skill_1,
        MINIS.pilot.skill_1,
        MINIS.harpies.skill_1,
    ],
    levelup_list=[
        MINIS.quilboar,
        MINIS.footmen,
        MINIS.pilot,
        MINIS.darkspear_troll,
        MINIS.sylvanas_windrunner,
    ]
)
