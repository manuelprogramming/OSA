import matplotlib.pyplot as plt
import json
from unused.Anritsu_Wrapper import Anritsu_MS9740B


def main():
    with open('../Settings.json') as json_file:
        data = json.load(json_file)

    sampling_points = data["sampling_points"]
    start_wavelength = data["start_wavelength"]
    stop_wavelength = data["stop_wavelength"]
    visa_search_term = data["visa_search_term"]

    anri = Anritsu_MS9740B(visa_search_term)
    anri.set_start_stop_wavelength(start_wavelength, stop_wavelength)
    anri.set_sampling_points(sampling_points)

    anri.do_single_sweap()

    wavelength, trace = anri.get_data()

    plt.plot(wavelength, trace)
    plt.ylabel("Intensity [dBm]")
    plt.xlabel("Wavelength [nm]")
    plt.show()


if __name__ == '__main__':
    main()