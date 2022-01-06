from dataclasses import dataclass


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
        self.showDialog()
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

        set_setting("selected_file", filename)
        root.destroy()

        self.result.value = filename


def initialize() -> None:
    factory.register("select_file", SelectFile)

