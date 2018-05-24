from ok_funcs import RadDevice
from ok_analysis import *
import numpy as np
import matplotlib.pyplot as plt

class ListoMode(RadDevice):

    def __init__(self, run_mode = 5):
        self.run_mode = run_mode
        self.ch_to_examine = ch_to_examine

    def set_intervals(self, intvl = 1, cycle = 60, address = 0x0C):
        ep0Cwire = intvl + List_Cycle*(2**4)
        self.xem.SetWireInValue(address, ep0Cwire, 2**32-1)
        self.xem.UpdateWireIns()

    def run_listo(self):
        pass

    def coarsen_listo_data(self, listo_data):
        pass

    def plot_listo_data(self, listo_data):
        pass
