from dataclasses import dataclass
from typing import Tuple, Dict, List

import numpy as np

from osa import factory
from result import BaseResult
from ref_handler import load_only_max_ref
from cache_handler import load_only_array_results


@dataclass
class CalcShift:
    """
    Calculates the Shift from the reference data
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        ref_dict: Dict[str, List[float]] = load_only_max_ref()
        array_result: Tuple[np.array, np.array] = load_only_array_results()
        if not ref_dict:
            self.result.msg = "no maximum reference data"
            return self.result
        if not array_result:
            self.result.msg = "no data in cache retrieve data before calculating shift"
            return self.result

        wavelength_max, trace_max = array_result

        wavelength_ref_max = np.array(ref_dict["wavelength_max"])
        trace_ref_max = np.array(ref_dict["trace_max"])

        self._calc_shift(wavelength_ref_max, trace_ref_max, wavelength_max, trace_max)

        return self.result

    def _calc_shift(self,
                    wavelength_ref_max: np.array,
                    trace_ref_max: np.array,
                    wavelength_max: np.array,
                    trace_max: np.array):
        """
        calculates the Red and Blue shifts from a given reference wavelength and reflection
        :param wavelength_ref_max: np.array
        :param trace_ref_max: np.array
        :return: the shifted point as (wavelength_shift, reflection_shift)
        """
        if (wavelength_max.shape == wavelength_ref_max.shape) and (trace_max.shape == trace_ref_max.shape):
            self.result.value = (wavelength_ref_max - wavelength_max, trace_ref_max - trace_max)
            self.result.msg = f"shifts calculated: {self.result.value}"
        else:
            self.result.msg = "reference data must have same number of peaks"


def initialize() -> None:
    factory.register("calc_shift", CalcShift)