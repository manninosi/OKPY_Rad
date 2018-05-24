from ok_funcs import RadDevice
from ok_analysis import *
import numpy as np
import matplotlib.pyplot as plt


class CoinMode(RadDevice):
    """Class to set-up coincidence mode for radiation detection with FPGAs.

    WARNING: Some methods have hardcoded addresses for WireIns

    """

    def __init__(self, run_mode = 3):
        self.run_mode = run_mode
        self.mca_data = []
        self.data_acquired = 0
        self.peak_ind = []

    def set_pattern(self, pattern = '00000000'):
        pass

    def set_coin_window(self, coin_window = 100 , address = 0x0E):
        pass

    def run_coin_meas(self):
        pass

    .
    
