import sys
from dataclasses import dataclass

from osa import factory
from handlers.result import BaseResult
from handlers.file import reset_selected_file


@dataclass
class CloseApp:
    """
    Closes the Application
    """
    command: str
    result: BaseResult

    @staticmethod
    def do_work() -> None:
        reset_selected_file()
        print("Shutting down...")
        sys.exit(0)


def initialize() -> None:
    factory.register("close_app", CloseApp)
