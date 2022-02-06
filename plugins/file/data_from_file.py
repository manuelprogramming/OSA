from dataclasses import dataclass

from osa import factory
from handlers.result import BaseResult
from handlers.file import get_selected_file_path, selected_file_is_empty, check_file
from handlers.data import DataGetter


@dataclass
class DataFromFile:
    """
    Asks for a column or index of the selected file and returns them as arrayData
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        file_path = get_selected_file_path()
        file_is_valid, msg = check_file()
        if not file_is_valid:
            self.result.msg = msg
            return self.result
        self._get_from_file(file_path)
        return self.result

    def _get_from_file(self, file_path) -> None:
        getter: DataGetter = DataGetter(file_path)
        user_input: str = self._ask_get_data(getter.get_valid_sets())
        data = getter.get_data(user_input)
        if not data[0].all():
            self._fail_getting(user_input)
        else:
            self._success_getting(user_input)
            self.result.value = data

    def _success_getting(self, user_input: str):
        self.result.msg = f"Successfully retrieved data '{user_input}'"

    def _fail_getting(self, user_input):
        self.result.msg = f"Couldn't get data '{user_input}' was not found"

    @staticmethod
    def _ask_get_data(data_set: set) -> str:
        return input(f"What data you want to retrieve? Specify from {data_set} \n")


def initialize() -> None:
    factory.register("data_from_file", DataFromFile)