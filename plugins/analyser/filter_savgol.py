from dataclasses import dataclass
from typing import Tuple

import scipy.signal as sgn
import numpy as np

from osa import factory
from handlers.cache import load_only_array_results
from handlers.result import BaseResult
from handlers.file import get_setting


@dataclass
class SavGol:
    """
    uses the SciPy Savitzky-Golay-Filter to calculate the filtered trace data from the cache
    The length of the filter window (i.e., the number of coefficients). window_length must be less
    than or equal to the size of x.
    The order of the polynomial used to fit the samples. polyorder must be less than window_length.
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        array_result: Tuple[np.array, np.array] = load_only_array_results()
        if not array_result:
            self._fail_result()
            return self.result
        array_length = len(array_result[0])
        window_length = get_setting("savgol_settings")["window_length"]
        if array_length < window_length:
            self._fail_result_wrong_savgol_settings(array_length, window_length)
            return self.result
        self.result.value = (array_result[0], self._savgol_filter(array_result))
        self._success_result()
        return self.result

    def _savgol_filter(self, arg: Tuple[np.array, np.array]) -> np.array:
        """The length of the filter window. window_length must be a positive odd integer.
        The order of the polynomial used to fit the samples. poly_order must be less than window_length
        :param arg: the argument retrieved from the cache data
        :return filtered_trace: as 1-dim numpy array
        """
        raw_trace = arg[1]
        savgol_settings = get_setting("savgol_settings")
        self.filtered_reflection = sgn.savgol_filter(raw_trace,
                                                     savgol_settings["window_length"],
                                                     savgol_settings["poly_order"])
        return raw_trace

    def _fail_result(self) -> None:
        self.result.msg = "retrieve Data before filtering the with the Savitzky-Golay-Filter"

    def _fail_result_wrong_savgol_settings(self, array_length: int, window_length: int) -> None:
        self.result.msg = "For Savatzki-Golay-Filter the window_length must be smaller then length of the data array\n"\
                          f"Here array_length: {array_length}, window_length: {window_length}"

    def _success_result(self):
        self.result.msg = "Savatzki-Golay-Filter calculated and saved to cache"

def initialize():
    factory.register("filter_savgol", SavGol)
