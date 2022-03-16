from dataclasses import dataclass
from multiprocessing import Queue, Process
from os import path


from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult
from osa import factory
from handlers.file import get_selected_file_path, set_setting, get_saving_path, get_current_date_time_str
from handlers.repeated_sweep_saving_engine import run_thread_engine, repeated_sweep_save


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

        if not self._file_is_empty(file_path):
            print("Selected File was not empty created a new file")
            self._create_new_file()

        q = Queue()
        p = Process(target=run_thread_engine, args=(repeated_sweep_save, q))
        p.start()
        p.join()
        sweep_num = q.get()

        self.result.msg = f"Aborted sweeping and saving.\n{sweep_num} sweeps completed and saved to {file_path}"

        return self.result

    @staticmethod
    def _file_is_empty(file_path: str) -> bool:
        return path.getsize(file_path) == 0

    def _create_new_file(self):
        saving_path = self._get_new_selected_file_path()
        set_setting("selected_file", saving_path)
        with open(saving_path, "w"):
            pass

    def _get_new_selected_file_path(self):
        file_name = self._create_filename()
        base_path = get_saving_path()
        return path.join(base_path, file_name)

    @staticmethod
    def _create_filename():
        cur_time = get_current_date_time_str()
        return cur_time + ".csv"


def initialize() -> None:
    factory.register("repeated_sweep_save", RepeatedSweepSave)


