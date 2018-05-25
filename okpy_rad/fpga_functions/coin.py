from ok_funcs import RadDevice
from ok_analysis import *
import numpy as np
import matplotlib.pyplot as plt


class CoinMode(RadDevice):
    """Class to set-up coincidence mode for radiation detection with FPGAs.

    Coincidence window, channels
    WARNING: Some methods have hardcoded addresses for WireIns

    """

    def __init__(self, run_mode = 3, ch_to_examine = [1,3,5,6]):
        self.run_mode = run_mode
        self.ch_to_examine = ch_to_examine
        self.peak_ind = []

    def set_ch_to_examine(self, ch_to_examine):
        """Updates list for channels to examine for coincidence
        """
        self.ch_to_examine = ch_to_examine


    def run_coin_meas_energy(self):
        pass

    def run_coin_meas_pulse(self):
        pass

    def plot_coin_data(self, data):
        pass
