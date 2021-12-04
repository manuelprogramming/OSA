from dataclasses import dataclass

import numpy as np

from osa import factory
from handlers.result import BaseResult
from handlers.ref import load_ref_data


@dataclass
class LoadRef:
    """
    Loads the saved reference data
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        ref_dict = load_ref_data()
        if not ref_dict:
            self.result.msg = "retrieve data before saving it as reference"
            return self.result

        ref_values = [value for value in ref_dict.values()]
        wavelength_ref = np.array(ref_values[0])
        trace_ref = np.array(ref_values[1])

        self._success_result(wavelength_ref, trace_ref)

        return self.result

    def _success_result(self, wavelength_ref: np.array, trace_ref: np.array) -> None:
        self.result.msg = f"reference data is \n" \
                          f"wavelength_ref:{wavelength_ref}\n" \
                          f"trace_ref: {trace_ref}\n"
        self.result.value = (wavelength_ref, trace_ref)


def initialize() -> None:
    factory.register("load_ref", LoadRef)
