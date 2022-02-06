from dataclasses import dataclass
import matplotlib.pyplot as plt
import pandas as pd
from os import path

from osa import factory
from handlers.result import BaseResult
from handlers.file import get_selected_file_path, check_file
from handlers.plotting import format_plot
from handlers.data import DataPlotter


@dataclass
class PlotFromFile:
    """
    Plots the Data from the last file created in the saved_data folder.
    """
    command: str
    result: BaseResult

    def do_work(self) -> BaseResult:
        file_path = get_selected_file_path()
        file_is_valid, msg = check_file()
        if not file_is_valid:
            self.result.msg = msg
            return self.result
        self._plot_from_file(file_path)
        self.result.msg = "plotted from file successfully"
        return self.result

    @format_plot
    def _plot_from_file(self, file_path) -> None:
        plotter: DataPlotter = DataPlotter(file_path)
        plotter.plot_data()


def initialize() -> None:
    factory.register("plot_from_file", PlotFromFile)
