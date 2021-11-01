from dataclasses import dataclass
from typing import Tuple
import numpy as np


from osa import factory


@dataclass
class DummyData:
    """
    Creates some random dummy data for testing purpose
    """
    command: str

    def do_work(self, settings, *args) -> Tuple[np.array, np.array]:
        sampling_points = settings["sampling_points"]
        start_wave = settings["start_wavelength"]
        stop_wave = settings["stop_wavelength"]
        wave_length = np.linspace(start_wave, stop_wave, sampling_points)
        trace = np.random.random_sample(sampling_points)-50
        return wave_length, trace


def initialize() -> None:
    factory.register("dummy_data", DummyData)