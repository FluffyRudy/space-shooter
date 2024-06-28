from typing import Union, Literal
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
        self.__init_ship_data()

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

    def write_player_data(self, data: dict):
        self.__ship_data.get("player").update(data)
        self.__write_to_file()

    def write_current_level(self, level: int):
        self.__ship_data["current_level"] = level
        self.__write_to_file()

    def __write_to_file(self):
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

    def get_ship_data(self) -> dict:
        return self.__ship_data

    def get_player_data(self):
        return Storage.get_ship_data().get("player")

    def get_level_data(self, level: int):
        return Storage.get_ship_data().get("levels").get(f"{level}")

    def get_current_level(self):
        return Storage.get_ship_data().get("current_level")

    def get_enemy_data(self, type_: Literal["shooter", "self_killer"]):
        return Storage.get_ship_data().get("enemies").get(type_)


Storage = StorageHandler()
