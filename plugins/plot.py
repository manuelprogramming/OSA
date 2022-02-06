import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt
from typing import Tuple

from osa import factory
from handlers.result import BaseResult
from handlers.cache import load_only_array_results
from handlers.plotting import format_plot
from handlers.file import get_setting, check_file


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

        plot_format: str = self._get_plot_fmt(trace)
        self._plot(wavelength, trace, plot_format)

        self.result.msg = "data plotted"
        self.result.value = array_result
        return self.result

    @staticmethod
    @format_plot
    def _plot(wavelength: np.array, trace: np.array, plot_format: str) -> None:
        plt.plot(wavelength, trace, plot_format)

    @staticmethod
    def _same_length(wavelength: np.array, trace: np.array) -> bool:
        return len(trace) == len(wavelength)

    @staticmethod
    def _get_plot_fmt(trace: np.array) -> str:
        if len(trace) <= get_setting("max_length_ref_data"):
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
