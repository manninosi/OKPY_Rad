from ok_funcs import RadDevice
from ok_analysis import *
import numpy as np
import matplotlib.pyplot as plt

class ScopeMode(RadDevice):
    """Creates object that is run in "Scope Mode" to look at pulses coming
    into the FPGA.
    """

    def __init__(self, run_mode = 1, scope_samples = 2**12):
        self.run_mode = run_mode
        self.data_acquired = 0
        self.pulse_data = []
        self.scope_samples = scope_samples

    def get_single_pulse(self, ch_select = 1):
        """Captures a single pulse"""
        #Set run mode to Oscilloscope
        self.xem.SetWireInValue(0x01, self.run_mode, 2**3-1)
        self.xem.UpdateWireIns()
        #Get ready signal to read out scope data
        self.xem.UpdateWireOuts()
        ready = bit_chop(self.xem.GetWireOutValue(0x21),ch_select, 1, 32)

        while ready == 0:
            self.xem.UpdateWireOuts()
            ready = bit_chop(self.xem.GetWireOutValue(0x21),ch_select, 1, 32)

        self.xem.ActivateTriggerIn(0x40,1)#Start Scope State Machine
        Buff_osc = bytearray('\x00'*self.scope_samples*4)
        self.xem.ReadFromPipeOut(ch_select+160, Buff_osc)
        Pulse = pipeout_assemble(Buff_osc, 4)

        #Set mode back to "stop"
        self.xem.SetWireInValue(0x01, 0, 2**3-1)
        self.xem.UpdateWireIns()
        return Pulse

    def get_pulse_data(self, num_pulses = 1000, plot = 1):
        """Continuous pulse data that can be plotted
        num_pulses(int): How many pulses to plot
        plot(bool):
            True: Continuous plotting of each pulse
            False: No plotting, but data is still captured
        """
        #Set run mode to Oscilloscope
        self.xem.SetWireInValue(0x01, self.run_mode, 2**3-1)
        self.xem.UpdateWireIns()
        #Get ready signal to read out scope data
        self.xem.UpdateWireOuts()
        ready = bit_chop(self.xem.GetWireOutValue(0x21),ch_select, 1, 32)

        for i in range(num_pulses):
            while ready == 0:
                self.xem.UpdateWireOuts()
                ready = bit_chop(self.xem.GetWireOutValue(0x21),ch_select, 1, 32)

            self.xem.ActivateTriggerIn(0x40,1)#Start Scope State Machine
            Buff_osc = bytearray('\x00'*self.scope_samples*4)
            self.xem.ReadFromPipeOut(ch_select+160, Buff_osc)
            Pulse = pipeout_assemble(Buff_osc, 4)
            self.pulse_data.append(Pulse)
            if plot == 1:
                #Test plotting with real bit file
                self.plot_pulse()
        #Set mode back to "stop"
        self.xem.SetWireInValue(0x01, 0, 2**3-1)
        self.xem.UpdateWireIns()
        return Pulse

    def plot_pulse(self, pulse_data):
        plt.ion()
        fig = plot.figure()
        ax = fig.add_subplot(111)#Creates figure object
        line1, = ax.plot(pulse_data, range(pulse_data))
        ax.set_ylim(min(pulse_data)-10, max(pulse_data)+10)
        ax.set_xlim(0, len(pulse_data))
        fig.canvas.drag()
        plt.pause(0.005)

        return None
