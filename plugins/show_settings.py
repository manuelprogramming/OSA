from dataclasses import dataclass
from typing import Dict, Any

from osa import factory
from file_handler import get_settings_dict


@dataclass
class ShowSettings:
    """
    Shows the Settings from the settings.json file. These Are not the Settings of the osa
    """
    command: str

    def do_work(self, *args) -> Dict[int, Any]:
        return get_settings_dict()


def initialize() -> None:
    factory.register("show_settings", ShowSettings)
