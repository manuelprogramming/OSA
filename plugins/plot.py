import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt

from osa import factory
from typing import Tuple

@dataclass
class Plot:
    """
    Plots the Data from the Cache Perform "get_data" before executing
    """
    command: str

    def do_work(self, *args) -> str:
        arg: Tuple[np.array, np.array] = args[0]
        try:
            wavelength, intensity = args[0]
            self._plot(wavelength, intensity)
            return "data plotted"
        except ValueError:
            return "retrieve data before plotting"

    @staticmethod
    def _plot(wavelength: np.array, intensity: np.array) -> None:
        plt.plot(wavelength, intensity)
        plt.ylabel("Intensity [dBm]")
        plt.xlabel("Wavelength [nm]")
        plt.show()


def initialize() -> None:
    factory.register("plot", Plot)
