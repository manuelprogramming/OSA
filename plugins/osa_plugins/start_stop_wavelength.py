"""A Plugin extension extenxion that adds a bla character"""

from dataclasses import dataclass
from osa import factory
from osa.anritsu_wrapper import BaseAnritsu
from result import BaseResult

from file_handler import get_settings_dict


@dataclass
class StartStopWavelength:
    """
    Sets the starting and stopping wavelength read out from the settings.json file
    the Settings can be changed with the change_settings tools
    """
    command: str
    result: BaseResult
    anri: BaseAnritsu

    def do_work(self) -> BaseResult:
        settings = get_settings_dict()
        start = settings["start_wavelength"]
        stop = settings["stop_wavelength"]
        self._set_start_stop_wavelength(start, stop)
        self.result.msg = f"Start Stop Wavelength set to {start}-{stop}"
        return self.result

    def _set_start_stop_wavelength(self, start: float = 600, stop: float = 1800) -> None:
        self.anri.write(f"WSS {start},{stop}")


def initialize() -> None:
    factory.register("start_stop_wavelength", StartStopWavelength)