from dataclasses import dataclass
from typing import Tuple

from tkinter.filedialog import askopenfilename
from tkinter import Tk

from osa import factory
from handlers.result import BaseResult
from handlers.file import get_saving_path, set_setting


@dataclass
class SelectFile:
    """
    Opens a File Dialog for selecting a file
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        file_name = self.showDialog()
        self.result.value = file_name

        valid_file_types = (".csv", ".xlsx", ".xls", ".dat", ".DAT", ".txt")
        if not self.result.value.endswith(valid_file_types):
            self._fail_result(valid_file_types)
            return self.result

        set_setting("selected_file", file_name)
        self.result.msg = f"Selected the file {self.result.value}"

        return self.result

    def showDialog(self):
        root = Tk()
        file_type_filter = [("All types", ".*"),
                            ("CSV file", ".csv"),
                            ("Excel files", ".xlsx .xls"),
                            ("Data files", ".dat .DAT"),
                            ("Text files", ".txt")]
        saving_path = get_saving_path()
        filename = askopenfilename(filetypes=file_type_filter, initialdir=saving_path)

        root.destroy()

        return filename

    def _fail_result(self, valid_file_types: Tuple[str, ...]):
        self.result.msg = f"The file chosen has not a valid type. Valid Types are {valid_file_types}"


def initialize() -> None:
    factory.register("select_file", SelectFile)
