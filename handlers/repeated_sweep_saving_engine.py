from pynput import keyboard
from time import sleep

from threading import Thread
from multiprocessing import Process, Queue


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


if __name__ == '__main__':
    my_queue = Queue()
    p = Process(target=run_thread_engine, args=(do_looping, my_queue))
    p.start()
    p.join()
