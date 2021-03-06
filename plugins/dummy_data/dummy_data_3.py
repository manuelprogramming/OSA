from dataclasses import dataclass
import numpy as np
import pandas as pd

from osa import factory
from handlers.result import BaseResult
from handlers.file import get_bin_files_path


@dataclass
class DummyData3:
    """
    Creates some dummy data from csv.file for testing purpose
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        data = pd.read_csv(get_bin_files_path("dummy.csv"), index_col=0)
        wavelength = np.array(data.index)
        trace = np.array(data.iloc[:, 1])

        self.result.msg = "dummy data 3 created and saved to cache"
        self.result.value = (wavelength, trace)
        return self.result


def initialize() -> None:
    factory.register("dummy_data_3", DummyData3)