from dataclasses import dataclass

from osa import factory
from handlers.file import set_setting, get_setting
from handlers.result import BaseResult


@dataclass
class ChangeStartWavelength:
    """
    Change the start_wavelength in the settings.json file,
    wavelength (nm): 600.0 to 1750.0 Specify smaller value than Stop wavelength
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        start_wavelength = self.ask_start_wavelength()
        if isinstance(start_wavelength, str):
            self._fail_result(start_wavelength)
            return self.result
        self._change_start_wavelength(start_wavelength)
        return self.result

    def _change_start_wavelength(self, start_wavelength: float) -> None:
        stop_wavelength = get_setting("stop_wavelength")
        if not self._wavelength_is_valid(start_wavelength, stop_wavelength):
            self._fail_result(start_wavelength)
        else:
            set_setting("start_wavelength", start_wavelength)
            self._success_result(start_wavelength)

    def _success_result(self, start_wavelength: float) -> None:
        self.result.msg = f"number for start_wavelength changed to '{start_wavelength}'"
        self.result.value = start_wavelength

    def _fail_result(self, start_wavelength: float or str) -> None:
        self.result.msg = f"number for start_wavelength  invalid '{start_wavelength}'"
        self.result.value = start_wavelength

    @staticmethod
    def _wavelength_is_valid(start_wavelength: float, stop_wavelength: float) -> bool:
        return (600.0 <= start_wavelength <= 1750.0) and (start_wavelength < stop_wavelength)

    @staticmethod
    def ask_start_wavelength() -> int or str:
        ans = input("#### Start wavelength (nm) 600.0 to 1750.0 Specify smaller value than Stop wavelength.\n")
        try:
            return round(float(ans), 1)
        except ValueError:
            return ans


def initialize() -> None:
    factory.register("change_start_wavelength", ChangeStartWavelength)