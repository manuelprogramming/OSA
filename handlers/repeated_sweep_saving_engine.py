from pynput import keyboard
from time import sleep

from threading import Thread
from multiprocessing import Process, Queue
import numpy as np
import pandas as pd

from handlers.file import get_setting, get_selected_file_path, get_visa_search_term
from osa.anritsu_wrapper import Anritsu

# The key combinations to look for
COMBINATIONS = [
    {keyboard.Key.ctrl_l, keyboard.KeyCode(vk=66)}  # shift + a (see below how to get vks)
]


def execute(my_queue):
    """ My function to execute when a combination is pressed """
    sweeping = "Stopped"
    my_queue.put(sweeping)


# The currently pressed keys (initially empty)
pressed_vks = set()


def get_vk(key):
    """
    Get the virtual key code from a key.
    These are used so case/shift modifications are ignored.
    """
    return key.vk if hasattr(key, 'vk') else key.value.vk


def is_combination_pressed(combination):
    """ Check if a combination is satisfied using the keys pressed in pressed_vks """
    return all([get_vk(key) in pressed_vks for key in combination])


def on_press(key, sweep_q: Queue):
    """ When a key is pressed """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.add(vk)  # Add it to the set of currently pressed keys

    for combination in COMBINATIONS:  # Loop though each combination
        if is_combination_pressed(combination):  # And check if all keys are pressed
            execute(sweep_q)  # If they are all pressed, call your function
            break  # Don't allow execute to be called more than once per key press


def on_release(key):
    """ When a key is released """
    vk = get_vk(key)  # Get the key's vk
    pressed_vks.remove(vk)  # Remove it from the set of currently pressed keys


def run_listener(sweep_q: Queue):
    """ Runs the Listener listens to the key Press Event"""
    with keyboard.Listener(on_press=lambda event: on_press(event, sweep_q)) as listener:
        listener.join()


def do_looping(my_queue: Queue):
    """ Function to test the engine without connection to ORCS"""
    while my_queue.empty():
        print("looping")
        sleep(0.5)


def run_thread_engine(loop_function: callable, sweep_q: Queue):
    t1 = Thread(target=run_listener, args=(sweep_q,), daemon=True)
    t1.start()
    t2 = Thread(target=loop_function, args=(sweep_q,))
    t2.start()


def repeated_sweep_save(q):
    anri = Anritsu(get_visa_search_term())
    rss = RepeatedSweepSaver(anri)

    memory_slot: str = get_setting("memory_slot") + "?"
    wavelength: np.array = rss.get_wavelength()
    file_path: str = get_selected_file_path()
    sweep_num = 0
    while q.empty():
        rss.do_single_sweep()
        trace: np.array = rss.get_data(memory_slot)
        if sweep_num == 0:
            rss.save_as_trace_data(file_path, wavelength, trace)
        else:
            rss.append_and_save_as_trace_data(file_path, trace, sweep_num)
        sweep_num += 1
        print(f"Completed sweep {sweep_num}")

    q.get()
    q.put(sweep_num)


class RepeatedSweepSaver:

    def __init__(self, anri):
        self.anri: Anritsu = anri

    def get_wavelength(self) -> np.array:
        sample_points = int(self.anri.query("MPT?"))
        start_wave = float(self.anri.query("STA?"))
        stop_wave = float(self.anri.query("STO?"))
        return np.linspace(start_wave, stop_wave, sample_points)

    def get_data(self, memory_slot: str) -> np.array:
        """
        gets the trace data from current memory_slot and wavelength of current measurement
        Returns: wavelength and trace bin from given Memory
        """
        trace = self.anri.query(memory_slot)  # getting trace Data
        return np.array([float(x) for x in trace.split()])

    def check_status(self) -> None:
        """
        when sweep_completed != 0 then it breaks the while loop and more commands can be send
        Returns: None
        """
        sweap_completed = 0
        self.anri.write("*CLS")
        while sweap_completed == 0:
            sweap_completed = int(self.anri.query(":STAT:EVEN:COND?"))
            sleep(0.5)

    def do_single_sweep(self) -> None:
        self.anri.write(":INIT")
        self.check_status()

    @staticmethod
    def save_as_trace_data(file_path: str, wavelength: np.array, trace: np.array) -> None:
        column_name = f"sweep_0"
        df = pd.DataFrame(data=trace, index=wavelength, columns=[column_name])
        df.index.name = "wavelength [nm]"
        df.to_csv(file_path)

    def append_and_save_as_trace_data(self, file_path: str, trace: np.array, column_number: int) -> None:
        df = pd.read_csv(file_path, index_col="wavelength [nm]")
        column_name = f"sweep_{column_number}"
        df[column_name] = trace
        df.to_csv(file_path)


if __name__ == '__main__':
    my_queue = Queue()
    p = Process(target=run_thread_engine, args=(do_looping, my_queue))
    p.start()
    p.join()
