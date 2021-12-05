from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np

from osa import factory
from handlers.result import BaseResult
from handlers.cache import load_only_array_results
from handlers.ref import save_as_ref_data
from handlers.file import get_max_length_ref_data


@dataclass
class SaveAsRef:
    """
    Saves The Calculated Arrays as Reference Data for shift calculations
    if arrays have a length smaller then 5 it will be saved as maxima data
    otherwise as raw data
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        array_result: Tuple[np.array, np.array] = load_only_array_results()
        if not array_result:
            self.result.msg = "retrieve data before saving it as reference"
            return self.result

        wavelength, trace = array_result
        ref_dict = self._create_ref_dict(wavelength, trace)
        save_as_ref_data(ref_dict)

        self.result.msg = "saved solution to ref data "
        self.result.value = (wavelength, trace)
        return self.result

    def _create_ref_dict(self, wavelength: np.array, trace: np.array) -> Dict[str, List[float]]:
        if len(wavelength) < get_max_length_ref_data():
            return {"wavelength_max": list(wavelength),
                    "trace_max": list(trace)}
        else:
            return {"wavelength": list(wavelength),
                    "trace": list(trace)}

def initialize() -> None:
    factory.register("save_as_ref", SaveAsRef)


