from dataclasses import dataclass


from osa import factory
from handlers.result import BaseResult
from handlers.file import create_new_folder, set_setting, get_setting


@dataclass
class ChangeSavingFolder:
    """
    Change the Saving Folder where the data is stored
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        folder_name = self.ask_saving_folder_name()
        saving_folder = get_setting("saving_folder")
        if saving_folder == folder_name and create_new_folder(saving_folder):
            self._fail_result(folder_name)
        else:
            set_setting("saving_folder", folder_name)
            self._change_saving_folder(folder_name)
        self.result.value = folder_name
        return self.result

    def _change_saving_folder(self, folder_name: str) -> None:
        if not create_new_folder(folder_name):
            self._success_result_folder_exists(folder_name)
        else:
            self._success_result(folder_name)

    def _success_result(self, folder_name: str) -> None:
        self.result.msg = f"New Saving Folder created '{folder_name}' and saved as saving folder"

    def _success_result_folder_exists(self, folder_name:str) -> None:
        self.result.msg = f"Folder '{folder_name}' already exist. '{folder_name}' selected as saving folder"

    def _fail_result(self, folder_name: str) -> None:
        self.result.msg = f"Folder '{folder_name}' already selected as saving folder \n" \
                          f"Folder '{folder_name}' was created if it didn't already existed"

    @staticmethod
    def ask_saving_folder_name() -> int or str:
        return input("#### What should be the name of the folder ?\n")


def initialize() -> None:
    factory.register("change_saving_folder", ChangeSavingFolder)