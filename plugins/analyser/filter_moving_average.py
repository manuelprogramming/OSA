from dataclasses import dataclass
from typing import Tuple

import numpy as np

from osa import factory
from cache_handler import load_only_array_results


@dataclass
class MovingAverage:
    """
    Calculates the moving average of reflection with the raw wavelength and raw trace from the cache
    """
    command: str

    def do_work(self) -> Tuple[np.array, np.array] or str:
        arg = load_only_array_results()
        if not arg:
            return "retrieve Data before calculating moving average"

        return self._moving_average(arg)

    def _moving_average(self, arg, window_size: int = 10) -> Tuple[np.array, np.array]:
        """
        :param window_size: sample points you want to take the average of
        """
        raw_wavelength = arg[0]
        raw_trace = arg[1]
        window = np.ones(int(window_size)) / float(window_size)
        power_average = np.convolve(raw_trace, window, 'same')
        filtered_trace = self._cut_data(power_average)
        filtered_wavelength = self._cut_data(raw_wavelength)
        return filtered_wavelength, filtered_trace

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
