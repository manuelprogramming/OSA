from dataclasses import dataclass

from osa import factory
from result import BaseResult
from file_handler import get_settings_dict


@dataclass
class ShowSettings:
    """
    Shows the Settings from the settings.json file. ! These Are not the Settings of the OSA !
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        self.result.msg = "Current Settings:\n" + str(get_settings_dict())
        self.result.value = get_settings_dict()
        return self.result


def initialize() -> None:
    factory.register("show_settings", ShowSettings)
