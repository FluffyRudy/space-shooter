from typing import Union, Literal, Optional, Any
import json
from json.decoder import JSONDecodeError
from pathlib import Path
from .datagen import generate_levels_data
from config import ROOT_DIR


class StorageHandler:
    __instance = None

    def __init__(self):
        """
        Initializes the StorageHandler instance. Sets up the storage path and initializes ship data.
        """
        if self.__instance is not None:
            return
        self.__storage_path: Path = ROOT_DIR / "src" / "storage" / "json"
        self.__write_default_data(num_levels=20)

        self.__game_data: dict = {}
        self.__init_game_data()

        self.__instance = self

    def __init_game_data(self) -> None:
        """
        Initializes ship data from the JSON file. If the file does not exist or is corrupted,
        it writes default data to the file.
        """
        game_data_path: Path = self.__storage_path / "ship-data.json"
        default_data_path: Path = self.__storage_path / "default-data.json"

        write_default_data: bool = False
        try:
            f_game_data = open(game_data_path, "r+")
            game_data: dict = json.load(f_game_data)
            self.__game_data = game_data
        except FileNotFoundError:
            Path(game_data_path).touch()
            f_game_data = open(game_data_path, "w")
            write_default_data = True
        except JSONDecodeError:
            write_default_data = True
        finally:
            if not write_default_data:
                f_game_data.close()
                return None
            with open(default_data_path, "r") as f_default_data:
                default_data: dict = json.load(f_default_data)
                json.dump(obj=default_data, fp=f_game_data, indent=4)
                self.__game_data = default_data
            f_game_data.close()

    def __write_default_data(self, num_levels: int):
        default_data_path: Path = self.__storage_path / "default-data.json"
        default_data = generate_levels_data(num_levels)

        with open(default_data_path, "w") as f_default_data:
            json.dump(obj=default_data, fp=f_default_data, indent=4)

    def write_player_data(self, data: dict) -> None:
        """
        Updates the player data in the ship data and writes it to the file.

        Args:
            data (dict): Dictionary containing player data to be updated.
        """
        self.__game_data.get("player").update(data)
        self.__write_to_file()

    def write_current_level(self, level: int) -> None:
        """
        Updates the current level in the ship data and writes it to the file.

        Args:
            level (int): The current level to be updated.
        """
        self.__game_data["current_level"] = level
        self.__write_to_file()

    def write_reward_point(self, level: int) -> None:
        """
        Updates the reward point of current level and write it to the file"

        Args:
            level (int): reward point of level to be update
        """
        level = str(level)
        self.__game_data["levels"][level]["reward_point"] = 0

    def write_weapon_data(self, type_: str, new_data: dict):
        self.__game_data[type_] = new_data
        self.__write_to_file()

    def __write_to_file(self) -> None:
        """
        Writes the current ship data to the JSON file.
        """
        game_data_path: Path = self.__storage_path / "ship-data.json"

        with open(game_data_path, "w") as f_game_data:
            try:
                json.dump(self.__game_data, f_game_data, indent=4)
            except (JSONDecodeError, FileNotFoundError):
                print("Couldn't save data")

    def reset_game_data(self) -> None:
        """
        Resets the ship data to the default values from the default data JSON file.
        """
        game_data_path: Path = self.__storage_path / "ship-data.json"
        default_data_path: Path = self.__storage_path / "default-data.json"

        with open(default_data_path, "r") as f_default_data:
            default_data: dict = json.load(f_default_data)
        with open(game_data_path, "w") as f_game_data:
            json.dump(default_data, f_game_data, indent=4)

    def get_game_data(self) -> dict:
        """
        Returns the current ship data.

        Returns:
            dict: Dictionary containing the ship data.
        """
        return self.__game_data

    def get_player_data(self) -> dict:
        """
        Returns the player data from the ship data.

        Returns:
            dict: Dictionary containing the player data.
        """
        return self.get_game_data().get("player")

    def get_level_data(self, level: int) -> dict:
        """
        Returns the data for a specific level from the ship data.

        Args:
            level (int): The level number to retrieve data for.

        Returns:
            dict: Dictionary containing the level data.
        """
        return self.get_game_data().get("levels").get(f"{level}")

    def get_current_level(self) -> int:
        """
        Returns the current level from the ship data.

        Returns:
            int: The current level.
        """
        return self.get_game_data().get("current_level")

    def get_enemy_data(self, type_: Literal["shooter", "self_killer"]) -> dict:
        """
        Returns the data for a specific type of enemy from the ship data.

        Args:
            type_ (Literal["shooter", "self_killer"]): The type of enemy to retrieve data for.

        Returns:
            dict: Dictionary containing the enemy data.
        """
        return self.get_game_data().get("enemies").get(type_)

    def get_weapons(self, type_: Literal["laser", "missile"]) -> dict:
        return self.get_all_weaponse().get(type_)

    def get_all_weaponse(self) -> dict:
        return self.get_game_data().get("weapons")

    def get_defence(self, type_: Literal["shield", "regan", "invincibility"]) -> dict:
        return self.get_all_defence().get(type_)

    def get_all_defence(self) -> dict:
        return self.get_game_data().get("defence")

    def write_weapon_data(self, type_, prop: str, new_value: int):
        self.__game_data["weapons"][type_][prop] = new_value


Storage = StorageHandler()
