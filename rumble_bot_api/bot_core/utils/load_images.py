from pprint import pprint
from pathlib import Path
from rumble_bot_api.desktop_automation_tool import ImageElement, Region, Position

RUMBLE_BOT_API_FOLDER = Path(__file__).resolve().parent.parent.parent
ASSETS_FOLDER = RUMBLE_BOT_API_FOLDER / 'assets'
MINIS_FOLDER = ASSETS_FOLDER / 'minis'
TOWER_IMAGE = ASSETS_FOLDER / 'other' / 'tower.png'

MINIS_SSIM = 0.8
MINIS_BOARD_REGION = Region(
    top_left=Position(x=330, y=830),
    bottom_right=Position(x=770, y=970)
)


def load_minis_from_images() -> list[str]:
    return [img.name.split('.')[0] for img in MINIS_FOLDER.iterdir() if img.is_file() and img.name.endswith('.png')]


def create_minis_dict(minis_board_region: Region = MINIS_BOARD_REGION, minis_ssim: float = MINIS_SSIM) -> dict:
    minis = load_minis_from_images()
    minis.sort()

    key_name = minis[0].split('_')[0]
    minis_dict = {key_name: {}}

    for name in minis:

        if key_name not in name:
            key_name = name.split('_')[0]
            minis_dict.update({key_name: {}})

        minis_dict[key_name].update(
            {
                name: ImageElement(
                    name=name,
                    path=str(MINIS_FOLDER / f'{name}.png'),
                    region=minis_board_region,
                    ssim=minis_ssim
                )
            }
        )

    return minis_dict


def get_lineup_from_minis_dict(minis_dict: dict, lineup: list[str]) -> dict:
    return {
        k: v.get(mini)
        for mini in lineup
        for k, v in minis_dict.items()
        if mini.split('_')[0] == k
    }


if __name__ == '__main__':
    print('============================================== MINIS ==============================================')
    mini_dict = create_minis_dict()
    pprint(mini_dict)
    print('\n\n\n============================================== LINEUP ==============================================')
    pprint(get_lineup_from_minis_dict(mini_dict, ['baron_1', 'harpies_1', 'pilot_0', 'prowler_0', 'necromancer_0']))
