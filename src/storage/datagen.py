def get_player_data():
    return {
        "health_count": 5,
        "speed": 5,
        "bullet_speed": 5,
        "bullet_damage": 1,
        "kill_damage_count": 5,
        "invincibility_cooldown_time": 1000,
        "bullet_cooldown_time": 200,
        "coins": 0,
    }


def get_weapon_data():
    return {
        "laser": {
            "damage": 1,
            "kill_after": 3000,
            "upgrades": {
                "upgrade_level": [1, 1],
                "max_upgrade_level": 5,
                "cost": 50,
                "cost_increase_rate": 2.0,
                "upgradable": ["damage", "kill_after"],
            },
        },
        "missile": {
            "speed": 5,
            "damage": 5,
            "count": 3,
            "upgrades": {
                "upgrade_level": [1, 1, 1],
                "max_upgrade_level": 5,
                "cost": 50,
                "cost_increase_rate": 2.0,
                "upgradable": ["speed", "damage", "count"],
            },
        },
    }


def get_defence_data():
    return {
        "shield": {
            "kill_after": 5000,
            "upgrades": {
                "upgrade_level": [1],
                "max_upgrade_level": 5,
                "cost": 50,
                "cost_increase_rate": 2.0,
                "upgradable": ["kill_after"],
            },
        },
        "regan": {
            "amount": 1,
            "kill_after": 0,
            "upgrades": {
                "upgrade_level": [1, 1],
                "max_upgrade_level": 5,
                "cost": 50,
                "cost_increase_rate": 2.0,
                "upgradable": ["amount", "kill_after"],
            },
        },
    }


def get_enemies_data():
    return {
        "shooter": {
            "health_count": 5,
            "speed": 2,
            "bullet_speed": 5,
            "bullet_damage": 1,
            "kill_damage_count": 5,
            "bullet_cooldown_time": 500,
        },
        "self_killer": {"speed": 8, "kill_damage_count": None},
    }


def generate_levels_data(num_levels):
    levels_data = {
        "current_level": 1,
        "player": get_player_data(),
        "weapons": get_weapon_data(),
        "defence": get_defence_data(),
        "enemies": get_enemies_data(),
        "levels": {},
    }

    for i in range(1, num_levels + 1):
        level = str(i)
        levels_data["levels"][level] = {
            "spawn_count": 5 + i,
            "max_spawn_count": 10 + 2 * i,
            "enemies": {
                "shooter": (1 - i * 0.002),
                "self_killer": (i * 0.002),
            },
            "reward_point": 3,
        }

    return levels_data
