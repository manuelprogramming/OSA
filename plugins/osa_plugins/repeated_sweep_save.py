import numpy as np
from dataclasses import dataclass
from typing import Tuple

import pandas as pd

from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult
from osa import factory
from handlers.file import get_setting, get_selected_file_path
from time import sleep
from handlers.repeated_sweep_saving_engine import run_thread_engine
from multiprocessing import Queue, Process


@dataclass
class RepeatedSweepSave:
    """
    Does a repeated Sweep Plotting and saved the data after every Sweep to the selected File.
    Creates a Subprocess do to so. Pressing 'CTRL + B' will terminate the sweeping.
    """
    command: str
    result: BaseResult
    anri: BaseAnritsu

    @test_anri_connection
    def do_work(self) -> BaseResult:
        file_path: str = get_selected_file_path()
        print("Repeated Sweep Saving started. Press 'CTRL + B' to stop sweeping")

        sweep_num = self._start_process()

        self.result.msg = f"Aborted sweeping and saving.\n {sweep_num} sweeps completed and saved to {file_path}"

        return self.result

    def _start_process(self) -> int:
        q = Queue()
        p = Process(target=run_thread_engine, args=(self._repeated_sweep_save, q))
        p.start()
        p.join()
        sweep_num = q.get()
        return sweep_num

    def _repeated_sweep_save(self, q):
        memory_slot: str = get_setting("memory_slot") + "?"
        wavelength: np.array = self._get_wavelength()
        file_path: str = get_selected_file_path()
        sweep_num = 0
        while q.empty():
            sleep(1)  # Remove if possible
            self._do_single_sweep()
            trace: np.array = self._get_data(memory_slot)
            if sweep_num == 0:
                self._save_as_trace_data(file_path, wavelength, trace)
            else:
                self._append_and_save_as_trace_data(file_path, trace, sweep_num)
            sweep_num += 1
            print(f"Completed sweep {sweep_num}")

        q.get()
        q.put(sweep_num)



    def _get_wavelength(self) -> np.array:
        sample_points = int(self.anri.query("MPT?"))
        start_wave = float(self.anri.query("STA?"))
        stop_wave = float(self.anri.query("STO?"))
        return np.linspace(start_wave, stop_wave, sample_points)

    def _get_data(self, memory_slot: str) -> np.array:
        """
        gets the trace data from current memory_slot and wavelength of current measurement
        Returns: wavelength and trace bin from given Memory
        """
        trace = self.anri.query(memory_slot)  # getting trace Data
        return np.array([float(x) for x in trace.split()])

    def _check_status(self) -> None:
        """
        when sweep_completed != 0 then it breaks the while loop and more commands can be send
        Returns: None
        """
        sweap_completed = 0
        self.anri.write("*CLS")
        while sweap_completed == 0:
            sweap_completed = int(self.anri.query(":STAT:EVEN:COND?"))
            sleep(0.5)

    def _do_single_sweep(self) -> None:
        self.anri.write(":INIT")
        self._check_status()

    def _success_result(self, memory_slot: str, value: Tuple[np.array, np.array]) -> None:
        self.result.msg = f"data retrieved from memory_slot '{memory_slot}'"
        self.result.value = value

    def _save_as_trace_data(self, file_path: str, wavelength: np.array, trace: np.array) -> None:
        column_name = f"sweep_0"
        df = pd.DataFrame(data=trace, index=wavelength, columns=[column_name])
        df.index.name = "wavelength [nm]"
        df.to_csv(file_path)

    def _append_and_save_as_trace_data(self, file_path: str, trace: np.array, column_number: int) -> None:
        df = pd.read_csv(file_path, index_col="wavelength [nm]")
        column_name = f"sweep_{column_number}"
        df[column_name] = trace
        df.to_csv(file_path)


def initialize() -> None:
    factory.register("repeated_sweep_save", RepeatedSweepSave)
