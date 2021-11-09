import numpy as np
from dataclasses import dataclass
from typing import Tuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from osa.anritsu_wrapper import BaseAnritsu, Anritsu
from result import BaseResult
from osa import factory
from file_handler import get_settings_dict



@dataclass
class RepeatedSweep:
    """
    Performs a repeated sweep and plots the data read out in the memory_slot in realtime
    """
    command: str
    result: BaseResult
    anri: BaseAnritsu

    def do_work(self) -> BaseResult:
        plt.style.use("seaborn-whitegrid")
        self.anri.write("SRT")
        self._get_wavelength()
        ani = FuncAnimation(plt.gcf(), self._get_data, interval=250)
        plt.show()

        self.anri.write("SST")

        self.result.msg = "repeated Sweep Plot canceled"
        return self.result

    def _get_wavelength(self):
        sampling_points = int(self.anri.query("MPT?"))
        start_wave = float(self.anri.query("STA?"))
        stop_wave = float(self.anri.query("STO?"))
        self.wave_length = np.linspace(start_wave, stop_wave, sampling_points)

    def _get_data(self, i) -> None:
        """
        """
        memory_slot = get_settings_dict()["memory_slot"] + "?"

        trace = self.anri.query(memory_slot)  # getting trace Data
        trace = np.array([float(x) for x in trace.split()])

        plt.cla()

        plt.plot(self.wave_length, trace, label=memory_slot.replace("?", ""))
        plt.ylabel("Intensity [dBm]")
        plt.xlabel("Wavelength [nm]")
        plt.legend(loc='upper left')
        plt.tight_layout()


def initialize() -> None:
    factory.register("repeated_sweep", RepeatedSweep)


