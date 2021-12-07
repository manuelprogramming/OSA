import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult
from osa import factory
from handlers.file import get_setting
from handlers.plotting import format_ani_plot, interactive_off_on


@dataclass
class RepeatedSweep:
    """
    Performs a repeated sweep and plots the data read out in the memory_slot in 250ms intervals
    On closing the plot window the sweep is stopped
    """
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        # TODO: Sometimes the program crashes after closing the plot window

        self.anri.write("SRT")

        wavelength = self._get_wavelength()
        memory_slot = get_setting("memory_slot") + "?"

        self._do_plotting(wavelength, memory_slot)
        self.anri.write("SST")

        self.result.msg = "repeated Sweep stopped"
        return self.result

    def _get_wavelength(self):
        sampling_points = int(self.anri.query("MPT?"))
        start_wave = float(self.anri.query("STA?"))
        stop_wave = float(self.anri.query("STO?"))
        wavelength = np.linspace(start_wave, stop_wave, sampling_points)
        return wavelength

    @interactive_off_on
    def _do_plotting(self, wavelength, memory_slot):
        fig = plt.figure("RepeatedSweep")
        ani = FuncAnimation(fig, self._get_data, fargs=(wavelength, memory_slot), interval=500)
        plt.show()

    @format_ani_plot
    def _get_data(self, i, wavelength: np.array, memory_slot: str) -> None:
        trace = self.anri.query(memory_slot)  # getting trace Data
        trace = np.array([float(x) for x in trace.split()])
        plt.cla()
        plt.plot(wavelength, trace, label=memory_slot.replace("?", ""))


def initialize() -> None:
    factory.register("repeated_sweep", RepeatedSweep)


