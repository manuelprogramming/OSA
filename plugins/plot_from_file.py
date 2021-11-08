from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd
from os import path

from osa import factory
from result import BaseResult
from file_handler import get_latest_file_path


@dataclass
class PlotFromFile:
    """
    Plots the Data from the last file created in the saved_data folder.
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        file_path = get_latest_file_path()
        if not file_path:
            self.result.msg = "no files in directory"
            return self.result
        if path.getsize(file_path) == 0:
            self.result.msg = "file is empty no plotting possible"
            return self.result
        self._plot_from_file(file_path)
        self.result.msg = "plotted from file successful"
        return self.result

    @staticmethod
    def _plot_from_file(file_path) -> None:
        plt.style.use("seaborn-whitegrid")
        df = pd.read_csv(file_path, index_col=0)
        df.plot()
        plt.ylabel("Intensity [dBm]")
        plt.tight_layout()
        plt.show()



def initialize() -> None:
    factory.register("plot_from_file", PlotFromFile)
