"""A Plugin extension extenxion that adds a bla character"""

from dataclasses import dataclass
from osa import factory


@dataclass
class StartStopWavelength:
    """
    Sets the starting and stopping wavelength
    Args:
        start: Starting Wavelength in Nanometer 600nm minimum
        stop: Stopping Wavelength in Nanometer 1800 nmm maximum
    """
    anri: str
    command: str

    def do_work(self, settings) -> str:
        start = settings.pop("start_wavelength")
        stop = settings.pop("stop_wavelength")
        self._set_start_stop_wavelength(start, stop)
        return f"Start Stop Wavelength set to {start} {stop} nm"

    def _set_start_stop_wavelength(self, start: float = 600, stop: float = 1800) -> None:
        self.anri.write(f"WSS {start},{stop}")


def initialize() -> None:
    factory.register("start_stop_wavelength", StartStopWavelength)