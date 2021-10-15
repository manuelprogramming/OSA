"""A Plugin extension extenxion that adds a bla character"""

from dataclasses import dataclass
from osa import factory


@dataclass
class StartStopWavelength:

    anri: str
    name: str

    def do_work(self, *args) -> None:
        start, stop = args
        # self._set_start_stop_wavelength(start, stop)
        print("Start Stop Wavelength set")

    def _set_start_stop_wavelength(self, start: float = 600, stop: float = 1800) -> None:
        """
        Sets the starting and stopping wavelength
        Args:
            start: Starting Wavelength in Nanometer 600nm minimum
            stop: Stopping Wavelength in Nanometer 1800 nmm maximum

        Returns: None

        """
        self.anri.write(f"WSS {start},{stop}")


def initialize() -> None:
    factory.register("start_stop_wavelength", StartStopWavelength)