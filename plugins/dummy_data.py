from dataclasses import dataclass
import numpy as np


from osa import factory
from result import BaseResult
from file_handler import get_settings_dict


@dataclass
class DummyData:
    """
    Creates some random dummy bin for testing purpose
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        settings = get_settings_dict()
        sampling_points = settings["sampling_points"]
        start_wave = settings["start_wavelength"]
        stop_wave = settings["stop_wavelength"]
        wave_length = np.linspace(start_wave, stop_wave, sampling_points)
        trace = np.random.random_sample(sampling_points)-50

        self.result.msg = "dummy data created"
        self.result.value = (wave_length, trace)
        return self.result


def initialize() -> None:
    factory.register("dummy_data", DummyData)