import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt


class ANDO_AQ6317B:
    """
    Hardware wrapper for ANDO AQ6317B Optical Spectrum Analyzer

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

    def set_timeout(self, milliseconds):
        """
        Sets the timeout of the instrument in milliseconds.

        Args:
            milliseconds(float): The timeout in milliseconds
        """
        self.inst.timeout = milliseconds

    def get_spectrum(self, channel='A'):
        """
        Returns the measured spectrum from a single reading of the instrument.
        Aliases to acquire

        Returns:
            tuple of arrays:
                The first array contains the wavelengths in nanometers.
                The second array contains the optical power in dBm.
        """
        power_string = self.inst.query('LDAT%s' % channel)
        power = np.array(power_string[:-2].split(','))
        power = power.astype(np.float64)[2:]

        wavelength_string = self.inst.query('WDAT%s' % channel)
        wavelength = np.array(wavelength_string[:-2].split(','))
        wavelength = wavelength.astype(np.float64)[2:]

        return wavelength, power


class Plotter:
    def __init__(self,wavelength, power):
        self.plot(wavelength, power)

    def plot(self, wavelength, power):
        plt.plot(wavelength,power)

        plt.ylabel("Power [Db]")
        plt.xlabel("Wavelength in nm")
        plt.show()


def main():
    # Setting Search Term
    visa_search_term = 'GPIB0::1::INSTR'
    ando = ANDO_AQ6317B(visa_search_term)
    # printing basic info
    print(ando.identify())

    wavelength, power = ando.get_spectrum()

    # Plotting Data
    Plotter(wavelength, power)


if __name__ == '__main__':
    main
