import numpy as np
from dataclasses import dataclass
from typing import Tuple
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from osa.anritsu_wrapper import BaseAnritsu
from result import BaseResult
from osa import factory
from file_handler import get_settings_dict



@dataclass
class RepeatedSweepPlot:
    """
    Performs a repeated sweep and plots the data read out in the memory_slot in realtime
    """
    command: str
    result: BaseResult
    anri: BaseAnritsu

    def do_work(self) -> BaseResult:
        plt.style.use("seaborn-whitegrid")
        ani = FuncAnimation(plt.gcf(), self._dummy_plot, interval=1000)

        plt.tight_layout()
        plt.show()

        self.result.msg = "repeated Sweep Plot canceled"

        return self.result

        # memory_slot = settings["memory_slot"] + "?"
        # return self._get_data(memory_slot)

    def _get_data(self, memory_slot: str = "DMB?") -> Tuple[np.array, np.array]:
        """
        gets the trace bin and wavelength of current measurement
        Returns: wavelength and trace bin from given Memory
        """
        trace = self.anri.query(memory_slot)  # getting trace Data
        trace = [float(x) for x in trace.split()]

        sampling_points = int(self.anri.query("MPT?"))
        start_wave = float(self.anri.query("STA?"))
        stop_wave = float(self.anri.query("STO?"))
        wave_length = np.linspace(start_wave, stop_wave, sampling_points)

        return wave_length, trace

    @staticmethod
    def _dummy_plot(i):
        settings = get_settings_dict()
        sampling_points = settings["sampling_points"]
        start_wave = settings["start_wavelength"]
        stop_wave = settings["stop_wavelength"]
        wave_length = np.linspace(start_wave, stop_wave, sampling_points)
        trace = np.random.random_sample(sampling_points) - 50

        plt.cla()

        memory_slot = settings["memory_slot"]

        plt.plot(wave_length, trace, label=memory_slot)

        plt.legend(loc='upper left')
        plt.tight_layout()


def initialize() -> None:
    factory.register("repeated_sweep_plot", RepeatedSweepPlot)
