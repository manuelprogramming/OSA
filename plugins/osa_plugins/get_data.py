import numpy as np
from dataclasses import dataclass
from typing import Tuple

from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from result import BaseResult
from osa import factory
from file_handler import get_settings_dict



@dataclass
class GetData:
    """
    Reads out the Measured Data in given memory_slot
    """
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        settings = get_settings_dict()
        memory_slot = settings["memory_slot"] + "?"
        self._get_data(memory_slot)
        return self.result

    def _get_data(self, memory_slot: str = "DMB?") -> None:
        """
        gets the trace data from current memory_slot and wavelength of current measurement
        Returns: wavelength and trace bin from given Memory
        """
        trace = self.anri.query(memory_slot)  # getting trace Data
        trace = [float(x) for x in trace.split()]

        sample_points = int(self.anri.query("MPT?"))
        start_wave = float(self.anri.query("STA?"))
        stop_wave = float(self.anri.query("STO?"))
        wave_length = np.linspace(start_wave, stop_wave, sample_points)
        value = (wave_length, trace)
        self._success_result(memory_slot, value)

    def _success_result(self, memory_slot: str, value: Tuple[np.array, np.array]) -> None:
        self.result.msg = f"data retrieved from memory_slot '{memory_slot}'"
        self.result.value = value


def initialize() -> None:
    factory.register("get_data", GetData)
