from dataclasses import dataclass
from typing import Any
from pathlib import Path
from os import path
from datetime import datetime

from osa import factory
from file_handler import get_settings_dict


@dataclass
class CreateNewFile:
    """
    Creates a new file in the saving_folder given in the settings.json file.
    the file name format is also read out from the settings.json file
    """
    command: str

    def do_work(self) -> Any:
        settings = get_settings_dict()
        saving_path = self._get_saving_path(settings)
        with open(saving_path, "w"):
            pass
        return "new file created"

    def _get_saving_path(self, settings):
        folder_name = self._get_folder_name(settings)
        path_of_file = Path(path.dirname(__file__))
        base_path = path_of_file.parent.absolute()
        return path.join(base_path, folder_name)

    def _get_folder_name(self, settings):
        saving_folder = settings["saving_folder"]
        cur_time = self._get_date_time(settings)
        return saving_folder + "\\" + cur_time + ".csv"

    @staticmethod
    def _get_date_time(settings):
        file_name_format = settings["file_name_format"]
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime(file_name_format)
        return timestampStr


def initialize() -> None:
    factory.register("create_new_file", CreateNewFile)