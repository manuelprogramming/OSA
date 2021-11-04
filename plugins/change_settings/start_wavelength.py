from dataclasses import dataclass
from typing import Tuple
import json


from osa import factory
from file_handler import get_settings_dict, get_settings_path


@dataclass
class ChangeStartWavelength:
    """
    Change the start_wavelength in the settings.json file,
    wavelength (nm): 600.0 to 1750.0 Specify smaller value than Stop wavelength
    """
    command: str

    def do_work(self, *args) -> Tuple[str, int]:
        settings = get_settings_dict()
        start_wavelength = self.ask_start_wavelength()
        return self._change_start_wavelength(start_wavelength, settings)

    def _change_start_wavelength(self, start_wavelength, settings) -> Tuple[str, int]:
        stop_wavelength = settings["stop_wavelength"]
        if self._wavelength_is_valid(start_wavelength, stop_wavelength):
            settings["start_wavelength"] = start_wavelength
            with open(get_settings_path(), "w", encoding='utf-8') as file:
                json.dump(settings, file, indent=4)
            return "number for start_wavelength changed to", start_wavelength
        else:
            return "number for start_wavelength  invalid", start_wavelength

    @staticmethod
    def _wavelength_is_valid(start_wavelength: float, stop_wavelength:float) -> bool:
        return (600.0 <= start_wavelength <= 1750.0) and (start_wavelength < stop_wavelength)

    @staticmethod
    def ask_start_wavelength() -> int or str:
        print("#### Start wavelength (nm) 600.0 to 1750.0 Specify smaller value than Stop wavelength.")
        ans = input()
        try:
            return round(float(ans), 1)
        except ValueError:
            return ans


def initialize() -> None:
    factory.register("change_start_wavelength", ChangeStartWavelength)