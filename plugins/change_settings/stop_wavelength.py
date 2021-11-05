from dataclasses import dataclass
from typing import Tuple
import json


from osa import factory
from file_handler import get_settings_dict, get_settings_path


@dataclass
class ChangeStopWavelength:
    """
    Change the stop_wavelength in the settings.json file,
    wavelength (nm): 600.0 to 1750.0 Specify bigger value than Start wavelength
    """
    command: str

    def do_work(self) -> Tuple[str, int]:
        settings = get_settings_dict()
        stop_wavelength = self.ask_start_wavelength()
        return self._change_start_wavelength(stop_wavelength, settings)

    def _change_start_wavelength(self, stop_wavelength, settings) -> Tuple[str, int]:
        start_wavelength = settings["start_wavelength"]
        if self._wavelength_is_valid(stop_wavelength, start_wavelength):
            settings["stop_wavelength"] = stop_wavelength
            with open(get_settings_path(), "w", encoding='utf-8') as file:
                json.dump(settings, file, indent=4)
            return "number for stop_wavelength changed to", stop_wavelength
        else:
            return "number for stop_wavelength  invalid", stop_wavelength

    @staticmethod
    def _wavelength_is_valid(stop_wavelength: float, start_wavelength: float) -> bool:
        return 600.0 <= stop_wavelength <= 1750.0 and start_wavelength < stop_wavelength

    @staticmethod
    def ask_start_wavelength() -> int or str:
        print("#### Stop wavelength (nm) 600.0 to 1750.0 Specify bigger value than start wavelength.")
        ans = input()
        try:
            return round(float(ans), 1)
        except ValueError:
            return ans


def initialize() -> None:
    factory.register("change_stop_wavelength", ChangeStopWavelength)