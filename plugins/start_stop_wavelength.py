"""A Plugin extension extenxion that adds a bla character"""

from dataclasses import dataclass
from osa import factory


@dataclass
class StartStopWavelength:
    """Sets the starting and stopping wavelength"""
    anri: str
    command: str

    def do_work(self, *args) -> str:
        start, stop = args
        self._set_start_stop_wavelength(start, stop)
        return "Start Stop Wavelength set"

    def _set_start_stop_wavelength(self, start: float = 600, stop: float = 1800) -> None:
        self.anri.write(f"WSS {start},{stop}")


def initialize() -> None:
    factory.register("start_stop_wavelength", StartStopWavelength)