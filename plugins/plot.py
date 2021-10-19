import numpy as np
from dataclasses import dataclass
from typing import Any
import matplotlib.pyplot as plt

from osa.anritsu_wrapper import BaseAnritsu
from osa import factory


@dataclass
class Plot:
    """
    Plots the Data from the Cache Perfom "get_data" before executing
    """
    anri: BaseAnritsu
    command: str

    def do_work(self, settings, *args) -> Any:
        if not args[0]:
            return "retrieve Data before plotting"
        wavelength, intensity = args[0]
        self._plot(wavelength, intensity)
        return None

    def _plot(self, wavelength: np.array, intensity: np.array) -> None:
        plt.plot(wavelength, intensity)
        plt.ylabel("Intensity [dBm]")
        plt.xlabel("Wavelength [nm]")
        plt.show()


def initialize() -> None:
    factory.register("plot", Plot)
