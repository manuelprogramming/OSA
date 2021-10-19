from dataclasses import dataclass
from osa import factory
from osa.anritsu_wrapper import BaseAnritsu


@dataclass
class StartStopWavelength:
    """
    Sets the starting and stopping wavelength
    Args:
        start: Starting Wavelength in Nanometer 600nm minimum
        stop: Stopping Wavelength in Nanometer 1800 nmm maximum
    """
    anri: BaseAnritsu
    command: str

    def do_work(self, settings, *args) -> str:
        start = settings["start_wavelength"]
        stop = settings["stop_wavelength"]
        self._set_start_stop_wavelength(start, stop)
        return f"Start Stop Wavelength set to {start} {stop} nm"

    def _set_start_stop_wavelength(self, start: float = 600, stop: float = 1800) -> None:
        self.anri.write(f"WSS {start},{stop}")


def initialize() -> None:
    factory.register("start_stop_wavelength", StartStopWavelength)