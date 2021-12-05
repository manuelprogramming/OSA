from dataclasses import dataclass
import numpy as np


from osa import factory
from handlers.result import BaseResult
from handlers.file import get_setting


@dataclass
class DummyData1:
    """
    Creates some random dummy bin for testing purpose
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        sampling_points = get_setting("sampling_points")
        start_wave = get_setting("start_wavelength")
        stop_wave = get_setting("stop_wavelength")
        wave_length = np.linspace(start_wave, stop_wave, sampling_points)
        trace = np.random.random_sample(sampling_points)-50

        self.result.msg = "dummy data created and saved to cache"
        self.result.value = (wave_length, trace)
        return self.result


def initialize() -> None:
    factory.register("dummy_data_1", DummyData1)