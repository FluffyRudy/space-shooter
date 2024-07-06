import sys


def generate_levels_data(num_levels):
    levels_data = {
        "current_level": 1,
        "player": {
            "health_count": 5,
            "speed": 5,
            "bullet_speed": 5,
            "bullet_damage": 1,
            "kill_damage_count": 5,
            "invincibility_cooldown_time": 1000,
            "bullet_cooldown_time": 200,
            "score": 0,
        },
        "weapons": {
            "laser": {"speed": 0, "damage": 1, "kill_after": 5000},
            "missile": {"speed": 5, "damage": 5, "count": 3},
        },
        "defence": {
            "shield": {"amount": 1, "kill_after": None},
            "regan": {"amount": 1, "kill_after": 0},
            "immunity": {"kill_after": 3000},
        },
        "enemies": {
            "shooter": {
                "health_count": 5,
                "speed": 2,
                "bullet_speed": 5,
                "bullet_damage": 1,
                "kill_damage_count": 5,
                "bullet_cooldown_time": 500,
            },
            "self_killer": {"speed": 8, "kill_damage_count": None},
        },
    }

    levels_data["levels"] = {}
    for i in range(1, num_levels + 1):
        level = str(i)
        levels_data["levels"][level] = {
            "spawn_count": 5 + i,
            "max_spawn_count": 10 + 2 * i,
            "enemies": {
                "shooter": max(0.5, round(1 - i * 0.02, 2)),
                "self_killer": min(round(i * 0.02, 2), 0.5),
            },
        }
    return levels_data
