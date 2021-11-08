from dataclasses import dataclass
from typing import Tuple

import numpy as np

from osa import factory
from cache_handler import load_only_array_results
from result import BaseResult


@dataclass
class MovingAverage:
    """
    Calculates the moving average of reflection with the raw wavelength and raw trace from the cache
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        array_result: Tuple[np.array, np.array] = load_only_array_results()
        if not array_result:
            self._fail_result()
            return self.result

        filtered_wavelength, filtered_trace = self._moving_average(array_result)

        self._success_result(filtered_wavelength, filtered_trace)

        return self.result

    def _moving_average(self,
                        array_result: Tuple[np.array, np.array],
                        window_size: int = 10) -> Tuple[np.array, np.array]:
        """
        :param window_size: sample points you want to take the average of
        """
        raw_wavelength = array_result[0]
        raw_trace = array_result[1]

        window = np.ones(int(window_size)) / float(window_size)
        trace_average = np.convolve(raw_trace, window, 'same')

        return self._cut_data(raw_wavelength), self._cut_data(trace_average)

    def _success_result(self, filtered_wavelength: np.array, filtered_trace: np.array) -> None:
        self.result.value = (filtered_wavelength, filtered_trace)
        self.result.msg = "moving average calculated and saved to cache"

    def _fail_result(self):
        self.result.msg = "retrieve Data before calculating moving average"

    @staticmethod
    def _cut_data(array, num_cut=10) -> np.array:
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
    factory.register("filter_moving_average", MovingAverage)
