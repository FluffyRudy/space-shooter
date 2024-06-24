from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
GRAPHICS_DIR = ROOT_DIR / 'graphics' / 'graphics'
ENEMY_SHIT_DIR = GRAPHICS_DIR / 'enemy_ship'
EXPLOSION_DIR = GRAPHICS_DIR / 'explosion'
PLAYER_SHIP_DIR = GRAPHICS_DIR / 'player_ship'
SPACE_BG_DIR = GRAPHICS_DIR / 'space_bg'

if __name__ == "__main__":
  all_dirs = [
    ROOT_DIR,
    GRAPHICS_DIR,
    ENEMY_SHIT_DIR,
    EXPLOSION_DIR,
    PLAYER_SHIP_DIR,
    SPACE_BG_DIR
  ]

  for dir_path in all_dirs:
    if not dir_path.exists():
      print(f"{dir_path} not found.")
