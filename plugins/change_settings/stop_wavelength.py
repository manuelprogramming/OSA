from dataclasses import dataclass

from osa import factory
from handlers.file import set_setting, get_setting
from handlers.result import BaseResult


@dataclass
class ChangeStopWavelength:
    """
    Change the stop_wavelength in the settings.json file,
    wavelength (nm): 600.0 to 1750.0 Specify bigger value than Start wavelength
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        stop_wavelength = self.ask_start_wavelength()
        if isinstance(stop_wavelength, str):
            self._fail_result(stop_wavelength)
            return self.result
        self._change_start_wavelength(stop_wavelength)
        return self.result

    def _change_start_wavelength(self, stop_wavelength: float) -> None:
        start_wavelength = get_setting("start_wavelength")
        if not self._wavelength_is_valid(stop_wavelength, start_wavelength):
            self._fail_result(stop_wavelength)
        else:
            set_setting("stop_wavelength", stop_wavelength)
            self._success_result(stop_wavelength)

    def _success_result(self, stop_wavelength) -> None:
        self.result.msg = f"number for stop_wavelength changed to '{stop_wavelength}'"
        self.result.value = stop_wavelength

    def _fail_result(self, stop_wavelength: float or str) -> None:
        self.result.msg = f"number for stop_wavelength  invalid '{stop_wavelength}'"
        self.result.value = stop_wavelength

    @staticmethod
    def _wavelength_is_valid(stop_wavelength: float, start_wavelength: float) -> bool:
        return 600.0 <= stop_wavelength <= 1750.0 and start_wavelength < stop_wavelength

    @staticmethod
    def ask_start_wavelength() -> int or str:
        ans = input("#### Stop wavelength (nm) 600.0 to 1750.0 Specify bigger value than start wavelength. \n")
        try:
            return round(float(ans), 1)
        except ValueError:
            return ans


def initialize() -> None:
    factory.register("change_stop_wavelength", ChangeStopWavelength)