from dataclasses import dataclass
from os import path
import subprocess

from osa import factory
from handlers.file import get_base_path
from handlers.result import BaseResult


@dataclass
class OpenDocumentation:
    """
    Opens the Operation Manuel PDF provided by Anritsu
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        manuel_path = "docs/ORCS_Documentation.pdf"
        full = path.join(get_base_path(), manuel_path)
        subprocess.Popen([full], shell=True)

        self.result.msg = "Documentation opening..."
        return self.result


def initialize() -> None:
    factory.register("open_documentation", OpenDocumentation)


