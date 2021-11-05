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
    Plots the Data from the Cache perform "get_data" before executing
    """
    command: str

    def do_work(self) -> Any:
        settings = get_settings_dict()
        saving_path = self._get_saving_path(settings)
        with open(saving_path, "w") as my_empty_csv:
            pass
        return "new file created"

    def _get_saving_path(self, settings):
        folder_name = self._get_folder_name(settings)
        path_of_file = Path(path.dirname(__file__))
        base_path = path_of_file.parent.absolute()
        return path.join(base_path, folder_name)

    def _get_folder_name(self, settings):
        saving_folder = settings["saving_folder"]
        cur_time = self._get_date_time()
        return saving_folder + "\\" + cur_time + ".csv"

    @staticmethod
    def _get_date_time():
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%Y-%b-%d,-,%H;%M;%S")
        return timestampStr


def initialize() -> None:
    factory.register("create_new_file", CreateNewFile)