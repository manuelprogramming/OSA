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

    def query(self, query_text: str) -> None:
        """
        Enter a query text for testing purpose
        Args:
            query_text:

        Returns:

        """
        self.inst.query(query_text)


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

    def start_single_sweep_1(self) -> None:
        """
        starts a single Sweep and saves it to csv
        Returns: None

        """
        end = self.inst.query("*CLS ; SSI ; ESR2?")
        while end == 0:
            end = self.inst.query("ESR2?")

        # self.inst.query("SVCSV")

    def start_single_sweep_2(self):
        self.inst.query("SSI ; *WAI ;")


def main():
    """IP Adress: 130.75.93.77
       Subnetz Maske: 255.255.255.0
       Host Name: OSA-UPCJ9GGPCMD
    """
    visa_search_term = 'TCPIP0::130.75.93.77::inst0::INSTR' # Example Term

    anri = Anritsu_MS9740B(visa_search_term)
    print(anri.identify())

    print(anri.get_start_stop_wavelength())
    print(anri.start_single_sweep_1())

if __name__ == '__main__':
    main()