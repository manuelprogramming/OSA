from dataclasses import dataclass

from osa import factory
from handlers.result import BaseResult
from handlers.file import get_selected_file_path, selected_file_is_empty
from handlers.data import DataDeleter


@dataclass
class DeleteColumn:
    """
    Asks for a column or index of the selected file and deletes this column or index
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        file_path = get_selected_file_path()
        if not file_path:
            self._fail_no_file()
            return self.result
        if selected_file_is_empty():
            self._fail_empty_file()
            return self.result
        self._delete(file_path)
        return self.result

    def _delete(self, file_path) -> None:
        deleter: DataDeleter = DataDeleter(file_path)
        to_delete: str = self._ask_deletion_data(deleter.get_valid_deletion_set())
        success: bool = deleter.delete_data(to_delete)
        if not success:
            self._fail_deletion(to_delete)
        else:
            self._success_deletion(to_delete)

    def _fail_no_file(self):
        self.result.msg = f"No file in the given directory"

    def _fail_empty_file(self):
        self.result.msg = f"Selected File {get_selected_file_path()} is empty"

    def _success_deletion(self, to_delete: str):
        self.result.msg = f"Successfully deleted {to_delete}"
        self.result.value = to_delete

    def _fail_deletion(self, to_delete):
        self.result.msg = f"Couldn't delete data no the {to_delete} was not found"

    @staticmethod
    def _ask_deletion_data(data_set: set) -> str:
        return input(f"What data you want to delete? Specify from {data_set} \n")


def initialize() -> None:
    factory.register("delete_from_file", DeleteColumn)