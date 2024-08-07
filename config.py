from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

ASSETS_DIR = ROOT_DIR / "assets"

# graphics
FONT_DIR = ASSETS_DIR / "fonts"
GRAPHICS_DIR = ASSETS_DIR / "graphics"
ENEMY_SHIP_DIR = GRAPHICS_DIR / "enemy_ship"
EXPLOSION_DIR = GRAPHICS_DIR / "explosion"
PLAYER_SHIP_DIR = GRAPHICS_DIR / "player_ship"
DEAD_EFFECT = PLAYER_SHIP_DIR / "dead_effect"
WEAPONS_DIR = GRAPHICS_DIR / "weapons"
DEFENCE_DIR = GRAPHICS_DIR / "defence"
SPACE_BG_DIR = GRAPHICS_DIR / "space_bg"
UI_DIR = GRAPHICS_DIR / "UI"
OBSTACLES_DIR = GRAPHICS_DIR / "obstacles"
POWEROPS_DIR = GRAPHICS_DIR / "powerops"

# sound
SOUND_PATH = ASSETS_DIR / "sounds"

if __name__ == "__main__":
    all_dirs = [
        ROOT_DIR,
        GRAPHICS_DIR,
        ENEMY_SHIP_DIR,
        EXPLOSION_DIR,
        PLAYER_SHIP_DIR,
        SPACE_BG_DIR,
        HEALTH_UI_DIR,
        OBSTACLES_DIR,
    ]

    for dir_path in all_dirs:
        if not dir_path.exists():
            print(f"{dir_path} not found.")
