from rumble_bot_api.bot_core.utils.common import set_logger
from rumble_bot_api import Processor, DropHandler, QuestsHandler, Predictor, MatchObject, MINIS
from config import TESSERACT_PATH, EMULATOR_PATH, EMULATOR_TITLE


BARON_PVE = MatchObject(
    hero=MINIS.baron_rivendare,
    lineup=[
        MINIS.huntress.skill_1,
        MINIS.ghoul.skill_1,
        MINIS.necromancer.skill_1,
        MINIS.darkspear_troll.skill_1,
        MINIS.pilot.skill_1,
        MINIS.harpies.skill_1,
        MINIS.baron_rivendare.skill_1
    ],
    levelup_list=[
        MINIS.quilboar,
        MINIS.baron_rivendare,
        MINIS.ghoul,
        MINIS.pilot,
        MINIS.darkspear_troll,
        MINIS.gryphon_rider,
        MINIS.blizzard,
        MINIS.whelp_eggs,
    ]
)

BARON_PVE2 = MatchObject(
    hero=MINIS.baron_rivendare,
    lineup=[
        MINIS.baron_rivendare.skill_1,
        MINIS.ghoul.skill_0,
        MINIS.bat_rider.skill_0,
        MINIS.darkspear_troll.skill_0,
        MINIS.gryphon_rider.skill_0,
        MINIS.pilot.skill_0,
        MINIS.quilboar.skill_0
    ],
    levelup_list=[
        MINIS.quilboar,
        MINIS.baron_rivendare,
        MINIS.ghoul,
        MINIS.pilot,
        MINIS.darkspear_troll,
        MINIS.gryphon_rider,
        MINIS.blizzard,
        MINIS.whelp_eggs,
        MINIS.tirion_fordring
    ]
)


TIRION_PVE = MatchObject(
    hero=MINIS.tirion_fordring,
    lineup=[
        MINIS.footmen.skill_0,
        MINIS.tirion_fordring.skill_0,
        MINIS.darkspear_troll.skill_0,
        MINIS.gryphon_rider.skill_0,
        MINIS.pilot.skill_0,
        MINIS.bat_rider.skill_0,
        MINIS.dark_iron_miner.skill_0,
    ],
    levelup_list=[
        MINIS.footmen,
        MINIS.pilot,
        MINIS.darkspear_troll,
        MINIS.tirion_fordring,
        MINIS.dark_iron_miner,
        MINIS.baron_rivendare
    ]
)


def main() -> None:

    set_logger(20)

    processor = Processor()
    processor.set_configurations(TESSERACT_PATH, EMULATOR_PATH, EMULATOR_TITLE)

    predictor = Predictor(processor.window)
    drop_handler = DropHandler(processor, predictor)
    quest = QuestsHandler(drop_handler)

    quest.set_quests_match_object(BARON_PVE)

    quest.main_loop()


if __name__ == '__main__':
    main()
