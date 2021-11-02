import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt

from osa import factory


@dataclass
class Plot:
    """
    Plots the Data from the Cache Perform "get_data" before executing
    """
    command: str

    def do_work(self, *args) -> str:
        arg = args[0]
        if not isinstance(arg, tuple):
            return "retrieve Data before plotting"

        wavelength, intensity = args[0]
        self._plot(wavelength, intensity)
        return "data plotted"

    @staticmethod
    def _plot(wavelength: np.array, intensity: np.array) -> None:
        plt.plot(wavelength, intensity)
        plt.ylabel("Intensity [dBm]")
        plt.xlabel("Wavelength [nm]")
        plt.show()


def initialize() -> None:
    factory.register("plot", Plot)
