from dataclasses import dataclass
from multiprocessing import Queue, Process


from osa.anritsu_wrapper import BaseAnritsu, test_anri_connection
from handlers.result import BaseResult
from osa import factory
from handlers.file import get_selected_file_path
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

        q = Queue()
        p = Process(target=run_thread_engine, args=(repeated_sweep_save, q))
        p.start()
        p.join()
        sweep_num = q.get()

        self.result.msg = f"Aborted sweeping and saving.\n{sweep_num} sweeps completed and saved to {file_path}"

        return self.result


def initialize() -> None:
    factory.register("repeated_sweep_save", RepeatedSweepSave)


