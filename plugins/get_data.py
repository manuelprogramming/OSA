import numpy as np
from dataclasses import dataclass
from typing import Tuple

from osa.anritsu_wrapper import BaseAnritsu
from osa import factory



@dataclass
class GetData:
    """
    Reads out the Measured Data in Given Channel
    """
    anri: BaseAnritsu
    command: str

    def do_work(self, settings) -> Tuple[np.array, np.array]:
        memory_slot = settings.pop("memory_slot") + "?"
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
