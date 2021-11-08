import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
from typing import Tuple

from osa import factory
from result import BaseResult
from cache_handler import load_only_array_results


@dataclass
class Plot:
    """
    Plots the Data from the Cache Perform "get_data" before executing
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        array_result: Tuple[np.array, np.array] = load_only_array_results()
        if not array_result:
            self.result.msg = "retrieve Data before plotting"
            return self.result

        wavelength, intensity = array_result
        self._plot(wavelength, intensity)
        self.result.msg = "data plotted"
        return self.result

    @staticmethod
    def _plot(wavelength: np.array, intensity: np.array) -> None:
        plt.style.use("seaborn-whitegrid")
        plt.plot(wavelength, intensity)
        plt.ylabel("Intensity [dBm]")
        plt.xlabel("Wavelength [nm]")
        plt.show()


def initialize() -> None:
    factory.register("plot", Plot)
