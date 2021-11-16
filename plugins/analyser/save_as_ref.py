from dataclasses import dataclass
import numpy as np
import pandas as pd

from osa import factory
from result import BaseResult
from file_handler import get_dummy_data_path


@dataclass
class SaveAsRef:
    """
    Saves The Calculated Maxima Arrays as Reference Data for shift calculations
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        data = pd.read_csv(get_dummy_data_path(), index_col=0)
        wavelength = np.array(data.index)
        trace = np.array(data.iloc[:, 1])

        self.result.msg = "saved solution to ref data "
        self.result.value = (wavelength, trace)
        return self.result


def initialize() -> None:
    factory.register("save_as_ref", SaveAsRef)