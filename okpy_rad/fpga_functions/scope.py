from ok_funcs import RadDevice
from ok_analysis import *
import numpy as np

class ScopeMode(RadDevice):
    def __init__(self, run_mode = 1):
        self.run_mode = run_mode
        self.data_acquired = 0

    def get_single_pulse(self):
        pass

    def get_pulse_data(self):
        pass

    def plot_pulse(self, pulse_data):
        pass
