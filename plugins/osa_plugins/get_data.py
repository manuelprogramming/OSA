import numpy as np
from dataclasses import dataclass
from typing import Tuple

from osa.anritsu_wrapper import BaseAnritsu
from osa import factory
from file_handler import get_settings_dict


@dataclass
class GetData:
    """
    Reads out the Measured Data in Given Channel
    """
    command: str
    anri: BaseAnritsu

    def do_work(self, *args) -> Tuple[np.array, np.array]:
        settings = get_settings_dict()
        memory_slot = settings["memory_slot"] + "?"
        return self._get_data(memory_slot)

    def _get_data(self, memory_slot: str = "DMB?") -> Tuple[np.array, np.array]:
        """
        gets the trace data and wavelength of current measurement
        Returns: wavelength and trace data from given Memory
        """
        trace = self.anri.query(memory_slot)  # getting trace Data
        trace = [float(x) for x in trace.split()]

        sample_points = int(self.anri.query("MPT?"))
        start_wave = float(self.anri.query("STA?"))
        stop_wave = float(self.anri.query("STO?"))
        wave_length = np.linspace(start_wave, stop_wave, sample_points)

        return wave_length, trace


def initialize() -> None:
    factory.register("get_data", GetData)