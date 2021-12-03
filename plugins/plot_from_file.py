from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd
from os import path

from osa import factory
from result import BaseResult
from file_handler import get_selected_file_path, get_settings_dict
from plotting import format_plot


@dataclass
class PlotFromFile:
    """
    Plots the Data from the last file created in the saved_data folder.
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        plt.style.use("seaborn-whitegrid")
        file_path = get_selected_file_path()
        if not file_path:
            self.result.msg = "no files in directory"
            return self.result
        if path.getsize(file_path) == 0:
            self.result.msg = "file is empty no plotting possible"
            return self.result
        print(file_path)
        self._plot_from_file(file_path)
        self.result.msg = "plotted from file successful"
        return self.result

    @format_plot
    def _plot_from_file(self, file_path) -> None:
        if self._is_points_data(file_path):
            self._plot_points_data(file_path)
        else:
            self._plot_trace_data(file_path)

        plt.legend()

    @staticmethod
    def _is_points_data(file_path) -> bool:
        df = pd.read_csv(file_path, index_col=0)
        return df.index.name == "bending_radius"


    @staticmethod
    def _plot_points_data(file_path):
        df = pd.read_csv(file_path, index_col=[0, 1])
        bending_radii = set([bending_radius for bending_radius in df.index.get_level_values('bending_radius')])
        for bending_radius in bending_radii:
            df_part = df.loc[bending_radius]
            y = df_part["trace [dBm]"].to_numpy()
            plt.plot(df_part.index.to_numpy(), y, "o", label=bending_radius)

    @staticmethod
    def _plot_trace_data(file_path):
        df = pd.read_csv(file_path, index_col=0)
        df.plot()
        # ax.set_ylabel("Intensity [dBm]")

def initialize() -> None:
    factory.register("plot_from_file", PlotFromFile)
