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
        my_arr = np.array([])
        if not arg:
            return "retrieve Data before plotting"
        if not (isinstance(arg[0], type(my_arr)) or isinstance(arg[1], type(my_arr))):
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
