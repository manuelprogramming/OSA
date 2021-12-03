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


if __name__ == '__main__':
    x = np.random.random(15)
    # myfunc(x)