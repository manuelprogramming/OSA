import matplotlib.pyplot as plt
import numpy as np


def format_plot(func):
    def func_wrapper(*args):
        func(*args)
        plt.ylabel("Intensity [dBm]")
        plt.xlabel("Wavelength [nm]")
        plt.tight_layout()
        plt.show()
        return func

    return func_wrapper


def format_ani_plot(func):
    def func_wrapper(*args):
        func(*args)
        plt.ylabel("Intensity [dBm]")
        plt.xlabel("Wavelength [nm]")
        plt.tight_layout()
        return func
    return func_wrapper


def interactive_off_on(func):
    def func_wrapper(*args):
        plt.ioff()
        func(*args)
        plt.ion()
        return func
    return func_wrapper


def config_matplotlib(debug_mode: bool) -> None:
    plt.style.use("seaborn-whitegrid")
    if not debug_mode:
        plt.ion()


if __name__ == '__main__':
    x = np.random.random(15)
