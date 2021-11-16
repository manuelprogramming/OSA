import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
from typing import Tuple
import multiprocessing as mp

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
            return self.result

        wavelength, trace = array_result
        if not self._same_length(wavelength, trace):
            self._fail_result_wrong_length(wavelength, trace)
            return self.result

        plot_format = self._get_plot_fmt(trace)
        self._plot(wavelength, trace, plot_format)

        self.result.msg = "data plotted"
        self.result.value = array_result
        return self.result


    @staticmethod
    def _plot(wavelength: np.array, trace: np.array, plot_format: np.array) -> None:
        plt.style.use("seaborn-whitegrid")
        plt.plot(wavelength, trace, plot_format)
        plt.ylabel("Intensity [dBm]")
        plt.xlabel("Wavelength [nm]")
        plt.tight_layout()
        plt.show()


    @staticmethod
    def _same_length(wavelength: np.array, trace: np.array) -> bool:
        return len(trace) == len(wavelength)

    @staticmethod
    def _get_plot_fmt(trace: np.array) -> str:
        if len(trace) <= 5:
            return "o"
        else:
            return "-"

    def _fail_result_no_data(self):
        self.result.msg = "retrieve Data before plotting"

    def _fail_result_wrong_length(self, wavelength, trace):
        self.result.msg = f"the data loaded from the cache must have the same length here: " \
                          f"{len(wavelength)}, {len(trace)}"


def initialize() -> None:
    factory.register("plot", Plot)
