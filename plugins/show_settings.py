from dataclasses import dataclass
from json import dumps

from osa import factory
from handlers.result import BaseResult
from handlers.file import get_settings_dict


@dataclass
class ShowSettings:
    """
    Shows the Settings from the settings.json file. ! These Are not the Settings of the OSA !
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        settings_str = str(dumps(get_settings_dict(), indent=4))
        self.result.msg = "Current Settings:\n" + settings_str
        self.result.value = get_settings_dict()
        return self.result


def initialize() -> None:
    factory.register("show_settings", ShowSettings)


if __name__ == '__main__':
    pass