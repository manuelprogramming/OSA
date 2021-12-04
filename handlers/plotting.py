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


def config_matplotlib(debug_mode: bool = None) -> None:
    if not debug_mode:
        debug_mode = False
    plt.style.use("seaborn-whitegrid")
    if not debug_mode:
        plt.ion()


if __name__ == '__main__':
    x = np.random.random(15)
