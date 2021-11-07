import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt

from osa import factory
from typing import Tuple
from cache_handler import load_only_array_results


@dataclass
class Plot:
    """
    Plots the Data from the Cache Perform "get_data" before executing
    """
    command: str

    def do_work(self) -> str:
        arg: Tuple[np.array, np.array] = load_only_array_results()
        if not arg:
            return "retrieve Data before plotting"

        wavelength, intensity = arg
        self._plot(wavelength, intensity)
        return "bin plotted"

    @staticmethod
    def _plot(wavelength: np.array, intensity: np.array) -> None:
        plt.style.use("seaborn-whitegrid")
        plt.plot(wavelength, intensity)
        plt.ylabel("Intensity [dBm]")
        plt.xlabel("Wavelength [nm]")
        plt.show()


def initialize() -> None:
    factory.register("plot", Plot)
