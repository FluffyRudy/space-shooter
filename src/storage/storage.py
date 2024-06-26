from typing import Union
import json
from json.decoder import JSONDecodeError
from pathlib import Path
from config import ROOT_DIR


class StorageHandler:
    __instance = None

    def __init__(self):
        if self.__instance is not None:
            return
        self.__storage_path = ROOT_DIR / "src" / "storage" / "json"
        self.__ship_data = {}
        self.__level_data = {}
        self.__init_ship_data()
        self.__init__level_data()

        self.__instance = self

    def __init_ship_data(self) -> None:
        ship_data_path = self.__storage_path / "ship-data.json"
        default_data_path = self.__storage_path / "default-data.json"

        write_default_data = False
        try:
            f_ship_data = open(ship_data_path, "r+")
            ship_data = json.load(f_ship_data)
            self.__ship_data = ship_data
        except FileNotFoundError:
            Path(ship_data_path).touch()
            write_default_data = True
        except JSONDecodeError:
            write_default_data = True
        finally:
            if not write_default_data:
                return None
            with open(default_data_path, "r") as f_default_data:
                default_data = json.load(f_default_data)
                json.dump(obj=default_data, fp=f_ship_data, indent=4)
                self.__ship_data = default_data
            f_ship_data.close()

    def __init__level_data(self):
        level_data_file = self.__storage_path / "level-data.json"

        if not level_data_file.exists():
            Path(level_data_file).touch()

        with open(file=level_data_file, mode="r") as f_level_data:
            try:
                level_data = json.load(f_level_data)
                self.__level_data = level_data
            except JSONDecodeError:
                pass

    def write_ship_data(self, data: dict):
        self.__ship_data["player"].update(data)
        ship_data_path = self.__storage_path / "ship-data.json"

        with open(ship_data_path, "w") as f_ship_data:
            try:
                json.dump(self.__ship_data, f_ship_data, indent=4)
            except (JSONDecodeError, FileNotFoundError):
                print("Couldnt save data")

    def reset_ship_data(self) -> None:
        ship_data_path = self.__storage_path / "ship-data.json"
        default_data_path = self.__storage_path / "default-data.json"

        with open(default_data_path, "r") as f_default_data:
            default_data = json.load(f_default_data)
        with open(ship_data_path, "w") as f_ship_data:
            json.dump(default_data, f_ship_data, indent=4)

    def get_ship_data(self):
        return self.__ship_data

    def get_level_data(self):
        return self.__level_data


Storage = StorageHandler()


def get_player_data():
    return Storage.get_ship_data().get("player")


def get_enemy_data():
    return Storage.get_ship_data().get("enemies")
