from dataclasses import dataclass
from typing import Tuple

import scipy.signal as sgn
import numpy as np

from osa import factory
from cache_handler import load_only_array_results


@dataclass
class SavGol:
    """
    uses the SciPy Savitzky-Golay-Filter to calculate the filtered trace data from the cache
    """
    command: str

    def do_work(self) -> Tuple[np.array, np.array] or str:
        arg = load_only_array_results()
        if not arg:
            return "retrieve Data before filtering the with the Savitzky-Golay-Filter "

        return arg[0], self._savgol_filter(arg)

    def _savgol_filter(self, arg: Tuple[np.array, np.array],
                       window_size: int = 101,
                       pol_order: int = 5) -> np.array:
        """
        :param arg: the argument retrieved from the cache data
        :param window_size: The length of the filter window. window_length must be a positive odd integer. If mode is
        :param pol_order: The order of the polynomial used to fit the samples. polyorder must be less than window_length
        :return filtered_reflection: as 1-dim numpy array
        """
        raw_trace = arg[1]
        self.filtered_reflection = sgn.savgol_filter(raw_trace, window_size, pol_order)
        return raw_trace


def initialize():
    factory.register("filter_savgol", SavGol)
