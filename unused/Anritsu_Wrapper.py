import pyvisa as visa
import numpy as np
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
            query_text: anything according to Remote Operation Manuel
        Returns:

        """
        return self.inst.query(query_text)

    def write(self, command_text: str) -> None:
        """
        For writing command
        Args:
            command_text: anything according to Remote Operation Manuel
        """
        self.inst.write(command_text)

    def identify(self):
        """
        Returns:
            str: The response from an `*IDN?`query.
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

    def get_start_stop_wavelength(self) -> (str, str):
        """
        Returns:start and stop wavelength of sweap

        """
        return self.query("WSS?")

    def check_status(self) -> None:
        """
        when sweapo_completed != 0 then it breaks the while loop and more commands can be send
        Returns: None
        """
        sweep_completed = 0
        self.write("*CLS")
        while sweep_completed == 0:
            sweep_completed = int(self.query(":STAT:EVEN:COND?"))
            print(f"Sweaping... {sweep_completed}")
            sleep(1)

    def do_single_sweep(self) -> None:
        """
        performs a single sweep and prints message on completion
        Returns: None
        """
        self.write(":INIT")
        self.check_status()
        print(f"Completed Sweep")

    def get_data(self, memory_slot: str = "DMB?") -> (np.array, np.array):
        """
        gets the trace data and wavelength of current measurement
        Returns: wavelength and trace data from given Memory
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




