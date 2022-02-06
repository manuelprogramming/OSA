from dataclasses import dataclass

from osa import factory
from handlers.result import BaseResult
from handlers.file import get_selected_file_path, selected_file_is_empty, check_file
from handlers.data import DataDeleter


@dataclass
class DeleteFromFile:
    """
    Asks for a column or index of the selected file and deletes this column or index
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        file_path = get_selected_file_path()
        file_is_valid, msg = check_file()
        if not file_is_valid:
            self.result.msg = msg
            return self.result
        self._delete(file_path)
        return self.result

    def _delete(self, file_path) -> None:
        deleter: DataDeleter = DataDeleter(file_path)
        user_input: str = self._ask_deletion_data(deleter.get_valid_sets())
        success: bool = deleter.delete_data(user_input)
        if not success:
            self._fail_deletion(user_input)
        else:
            self._success_deletion(user_input)

    def _success_deletion(self, user_input: str) -> None:
        self.result.msg = f"Successfully deleted {user_input}"
        self.result.value = user_input

    def _fail_deletion(self, user_input) -> None:
        self.result.msg = f"Couldn't delete data '{user_input}' was not found"

    @staticmethod
    def _ask_deletion_data(data_set: set) -> str:
        return input(f"What data you want to delete? Specify from {data_set} \n")


def initialize() -> None:
    factory.register("delete_from_file", DeleteFromFile)