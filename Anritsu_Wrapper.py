import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt


class Anritsu_MS9740B:
    """
    Hardware wrapper for Anritsu_MS9740B Optical Spectrum Analyzer

    Parameters:
        visa_search_term (str): The address that is passed to
            ``visa.ResourceManager().open_resource()``
    """
    def __init__(self, visa_search_term):
        rm = visa.ResourceManager()
        self.inst = rm.open_resource(visa_search_term)

    def identify(self):
        """
        Returns:
            str: The response from an ``*IDN?`` GPIB query.
        """
        return self.inst.query('*IDN?')

    def clear_all_registers(self) -> None:
        """
        Clears all the common registers
        """
        self.inst.query("*CLS")

    def set_start_stop_wavelength(self, start: float = 600, stop: float = 1800) -> None:
        """
        Sets the starting and stopping wavelength
        Args:
            start: Starting Wavelength in Nanometer 600nm minimum
            stop: Stopping Wavelength in Nanometer 1800 nmm maximum

        Returns: None

        """
        self.inst.query(f"WSS {start},{stop}")

    def get_start_stop_wavelength(self) -> (float, float):
        return self.inst.query("WSS?")

    def start_single_sweep(self, mode: int = 1) -> None:
        """
        starts a single Sweep and saves it to csv
        Args:
            mode: indicates two queries for testing reasons

        Returns: None

        """
        if mode == 1:
            end = self.inst.query("*CLS ; SSI ; ESR2?")
            while end == 0:
                end = self.inst.query("ESR2?")
            self.inst.query("SVCSV")
        elif mode == 2:
            self.inst.query("SSI ; *WAI ; SVCSV")


if __name__ == '__main__':
    visa_search_term = 'GPIB0::1::INSTR' # Example Term

    anri = Anritsu_MS9740B(visa_search_term)
    print(anri.identify())