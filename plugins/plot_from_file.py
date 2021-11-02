from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd
from os import path

from osa import factory
from file_handler import get_latest_file_path


@dataclass
class PlotFromFile:
    """
    Plots the Data from the Cache Perform "get_data" before executing
    """
    command: str

    def do_work(self, *args) -> str:
        file_path = get_latest_file_path()
        if path.getsize(file_path) == 0:
            return "file is empty no plotting possible"
        self._plot_from_file(file_path)
        return "data from file plotted"

    @staticmethod
    def _plot_from_file(file_path) -> None:
        df = pd.read_csv(file_path, index_col=0)
        df.plot()
        plt.ylabel("Intensity [dBm]")
        plt.show()



def initialize() -> None:
    factory.register("plot_from_file", PlotFromFile)
