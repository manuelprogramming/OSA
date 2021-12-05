from dataclasses import dataclass
from os import path

from osa import factory
from handlers.file import get_current_date_time_str, get_saving_path, set_setting
from handlers.result import BaseResult


@dataclass
class CreateNewFile:
    """
    Creates a new file in the saving_folder given in the settings.json file.
    the file name format is also read out from the settings.json file
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        saving_path = self._get_saving_path()
        set_setting("selected_file", saving_path)
        with open(saving_path, "w"):
            pass
        self.result.msg = f"new file created and selected in {saving_path}"
        return self.result

    def _get_saving_path(self):
        folder_name = self._create_filename()
        base_path = get_saving_path()
        return path.join(base_path, folder_name)

    def _create_filename(self):
        cur_time = get_current_date_time_str()
        return cur_time + ".csv"



def initialize() -> None:
    factory.register("create_new_file", CreateNewFile)


if __name__ == '__main__':
    tool = CreateNewFile("CNF", None)
    print(tool._get_saving_path())