from dataclasses import dataclass
from typing import Tuple

import numpy as np
from scipy import signal as sgn

from osa import factory
from handlers.cache import load_only_array_results
from handlers.result import BaseResult


@dataclass
class CalcMaxima:
    """
    Calculates the Maxima of reflection with the wavelength and trace from the cache
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        array_result: Tuple[np.array, np.array] = load_only_array_results()
        if not array_result:
            self._fail_result()
            return self.result

        wavelength, trace = array_result

        self._calc_maximum(wavelength, trace)
        self._success_result()
        return self.result

    def _calc_maximum(self, wavelength: np.array, trace: np.array) -> None:
        max_reflection_index, _ = sgn.find_peaks(trace, prominence=1)
        max_trace = trace[max_reflection_index]
        max_list_bool = self._create_max_bool_list(trace, max_trace)
        self.result.value = (wavelength[max_list_bool], max_trace)

    @staticmethod
    def _create_max_bool_list(trace: np.array, max_reflections: np.array) -> np.array:
        """
        internal Helping function for calculating the maximum Points
        :param max_reflections: the value for the maximum reflection
        :return: a list of boolean values
        """
        max_list_bool = sum(
            [np.where(trace == max_reflection, 1, 0) for max_reflection in
             max_reflections])
        max_list_bool = np.where(max_list_bool == 1, True, False)
        return max_list_bool

    def _success_result(self) -> None:
        self.result.msg = f"maxima calculated and saved to cache\n" \
                          f"maxima at {self.result.value}"

    def _fail_result(self):
        self.result.msg = "retrieve Data before calculating maxima"

    @staticmethod
    def _cut_data(array: np.array, num_cut: int = 10) -> np.array:
        """
        used to cut the data for the moving average filter
        :param array: 1-Dim numpy array what should be cutted
        :param num_cut: the number of datapoints to cut off
        :return: the cutted array
        """
        c = num_cut // 2
        array = array[c:-c]
        return array


def initialize():
    factory.register("calc_maxima", CalcMaxima)
