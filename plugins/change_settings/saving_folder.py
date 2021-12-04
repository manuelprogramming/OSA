from dataclasses import dataclass
import json


from osa import factory
from handlers.result import BaseResult
from handlers.file import get_settings_path, create_new_folder, get_settings_dict


@dataclass
class ChangeSavingFolder:
    """
    Change the Saving Folder where the data is stored
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        settings = get_settings_dict()
        folder_name = self.ask_saving_folder_name()
        if settings["saving_folder"] == folder_name:
            self._fail_result(folder_name)
        else:
            self._edit_settings_dict(folder_name, settings)
            self._change_saving_folder(folder_name)
        self.result.value = folder_name
        return self.result

    def _change_saving_folder(self, folder_name: str) -> None:
        if not create_new_folder(folder_name):
            self._success_result_folder_exists(folder_name)
        else:
            self._success_result(folder_name)

    def _edit_settings_dict(self, folder_name:str, settings: dict) -> None:#
        settings["saving_folder"] = folder_name
        with open(get_settings_path(), "w", encoding='utf-8') as file:
            json.dump(settings, file, indent=4)

    def _success_result(self, folder_name:str) -> None:
        self.result.msg = f"New Saving Folder created '{folder_name}' and saved as saving folder"

    def _success_result_folder_exists(self, folder_name:str) -> None:
        self.result.msg = f"Folder '{folder_name}' already exist. '{folder_name}' selcted as saving folder"

    def _fail_result(self, folder_name: str) -> None:
        self.result.msg = f"Folder '{folder_name}' already selected as saving folder \n"

    @staticmethod
    def ask_saving_folder_name() -> int or str:
        print("#### What should be the name of the folder ?")
        return input()


def initialize() -> None:
    factory.register("change_saving_folder", ChangeSavingFolder)