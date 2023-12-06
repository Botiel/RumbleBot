from test_flows.utils import init_processor
from rumble_bot_api.bot_core.handlers.hero_manager_handler import HeroManagerHandler
from time import sleep

if __name__ == '__main__':
    p = init_processor()
    m = HeroManagerHandler(p)
    m.switch_hero('tirion_fordring')
    sleep(3)
    m.switch_hero('baron_rivendare')
