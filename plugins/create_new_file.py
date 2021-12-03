from dataclasses import dataclass
from os import path
from datetime import datetime

from osa import factory
from file_handler import get_settings_dict, get_base_path, change_selected_file, get_current_date_time_str
from result import BaseResult


@dataclass
class CreateNewFile:
    """
    Creates a new file in the saving_folder given in the settings.json file.
    the file name format is also read out from the settings.json file
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        settings = get_settings_dict()
        saving_path = self._get_saving_path(settings)
        change_selected_file(saving_path)
        with open(saving_path, "w"):
            pass
        self.result.msg = f"new file created and selected in {saving_path}"
        return self.result

    def _get_saving_path(self, settings):
        folder_name = self._get_folder_name(settings)
        base_path = get_base_path()
        return path.join(base_path, folder_name)

    def _get_folder_name(self, settings):
        saving_folder = settings["saving_folder"]
        cur_time = get_current_date_time_str()
        return saving_folder + "\\" + cur_time + ".csv"



def initialize() -> None:
    factory.register("create_new_file", CreateNewFile)