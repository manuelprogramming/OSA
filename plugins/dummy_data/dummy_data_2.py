from dataclasses import dataclass
import numpy as np
import pandas as pd

from osa import factory
from handlers.result import BaseResult
from handlers.file import get_bin_path


@dataclass
class DummyData2:
    """
    Creates some dummy data from csv.file for testing purpose
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        data = pd.read_csv(get_bin_path("dummy.csv"), index_col=0)
        wavelength = np.array(data.index)
        trace = np.array(data.iloc[:, 0])

        self.result.msg = "dummy data 2 created and saved to cache"
        self.result.value = (wavelength, trace)
        return self.result


def initialize() -> None:
    factory.register("dummy_data_2", DummyData2)