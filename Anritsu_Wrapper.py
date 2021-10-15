import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
from time import sleep


class Anritsu_MS9740B:
    """
    Hardware wrapper for Anritsu_MS9740B Optical Spectrum Analyzer
    IP Adress: 130.75.93.77
       Subnetz Maske: 255.255.255.0
       Host Name: OSA-UPCJ9GGPCMD
    Parameters:
        visa_search_term (str): The address that is passed to
            ``visa.ResourceManager().open_resource()``
    """

    def __init__(self, visa_search_term):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(visa_search_term)

        print("Connected to ", self.identify())

    def query(self, query_text: str):
        """
        Enter a query text for testing purpose
        Args:
            query_text:

        Returns:

        """
        return self.inst.query(query_text)

    def write(self, command_text: str) -> None:
        """
        For writing command
        Args:
            command_text:
        """
        self.inst.write(command_text)

    def identify(self):
        """
        Returns:
            str: The response from an ``*IDN?`` GPIB query.
        """
        return self.query('*IDN?')

    def clear_all_registers(self) -> None:
        """
        Clears all the common registers
        """
        self.query("*CLS")

    def set_start_stop_wavelength(self, start: float = 600, stop: float = 1800) -> None:
        """
        Sets the starting and stopping wavelength
        Args:
            start: Starting Wavelength in Nanometer 600nm minimum
            stop: Stopping Wavelength in Nanometer 1800 nmm maximum

        Returns: None

        """
        self.write(f"WSS {start},{stop}")

    def get_start_stop_wavelength(self) -> (float, float):
        """
        Returns:start and stop wavelength of sweap

        """
        return self.query("WSS?")

    def start_single_sweep_1(self) -> None:
        """
        starts a single Sweep and saves it to csv
        Returns: None

        """

    def check_status(self) -> None:
        """
        when sweapo_completed != 0 then it breaks the while loop and more commands can be send
        Returns: None
        """
        sweap_completed = 0
        self.write("*CLS")
        while sweap_completed == 0:
            sweap_completed = int(self.query(":STAT:EVEN:COND?"))
            print(f"Sweaping... {sweap_completed}")
            sleep(1)

    def do_single_sweap(self) -> None:
        """
        perfomsn a single sweap and prints message on completion
        Returns: None
        """
        self.write(":INIT")
        self.check_status()
        print(f"Completed Sweap")

    def get_data(self, memory_slot: str = "DMB?") -> (np.array, np.array):
        """
        gets the trace data and wavewlnegth of current measurement
        Returns: wavelength and trace data from givcen Memory
        """
        trace = self.query(memory_slot)  # getting trace Data
        trace = [float(x) for x in trace.split()]

        sample_points = int(self.query("MPT?"))
        start_wave = float(self.query("STA?"))
        stop_wave = float(self.query("STO?"))
        wave_length = np.linspace(start_wave, stop_wave, sample_points)

        return wave_length, trace

    def set_sampling_points(self, sampling_points) -> None:
        """
        for setting sampling points
        Args:
            sampling_points: Number of sampling points {51|101|251|501|1001|2001|5001|10001|20001|50001}
        Returns: None
        """
        self.write(f"MPT {sampling_points}")


def main():
    sampling_points = 501  # 51|101|251|501|1001|2001|5001|10001|20001|50001
    start_wavelength = 1350
    stop_wavelength = 1450
    visa_search_term = 'TCPIP0::130.75.93.77::inst0::INSTR'

    anri = Anritsu_MS9740B(visa_search_term)
    anri.set_start_stop_wavelength(start_wavelength, stop_wavelength)
    anri.set_sampling_points(sampling_points)

    anri.do_single_sweap()

    wavelength, trace = anri.get_data()

    plt.plot(wavelength, trace)
    plt.ylabel("Intensity [dBm]")
    plt.xlabel("Wavelenght [nm]")
    plt.show()


if __name__ == '__main__':
    main()

