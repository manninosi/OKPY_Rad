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

        #Making plotting object
        self.make_figure = plt.figure()
        self.ax = self.make_figure.add_subplot(111)#Creates figure object
        self.line1, = self.ax.plot([],  [])


    def get_single_pulse(self, ch_select = 5):
        """Captures a single pulse"""
        #Set run mode to Oscilloscope
        self.xem.SetWireInValue(0x01, self.run_mode, 2**3-1)
        self.xem.UpdateWireIns()
        #Get ready signal to read out scope data
        self.xem.UpdateWireOuts()
        ready = bit_chop(self.xem.GetWireOutValue(0x21),ch_select, ch_select, 32)
        print ready
        while ready == 0:
            self.xem.UpdateWireOuts()
            ready = bit_chop(self.xem.GetWireOutValue(0x21),ch_select, ch_select, 32)

        self.xem.ActivateTriggerIn(0x40,1)#Start Scope State Machine
        Buff_osc = bytearray(self.scope_samples*4)
        self.xem.ReadFromPipeOut(ch_select+160, Buff_osc)
        Pulse = pipeout_assemble(Buff_osc, 4)
            osc_values = []
            for i in range(len(Pulse)):
                osc_values.append(bit_chop(Pulse[i], 13, 0, 32))
            self.pulse_data.append(osc_values)        #Set mode back to "stop"
        self.xem.SetWireInValue(0x01, 0, 2**3-1)
        self.xem.UpdateWireIns()
        return Pulse

    def get_pulse_data(self, num_pulses = 1000, plot = 1, ch_select = 5):
        """Continuous pulse data that can be plotted
        num_pulses(int): How many pulses to plot
        plot(bool):
            True: Continuous plotting of each pulse
            False: No plotting, but data is still captured
        """
        #Set run mode to Oscilloscope
        self.xem.SetWireInValue(0x01, self.run_mode, 2**3-1)
        self.xem.UpdateWireIns()
        self.xem.ActivateTriggerIn(0x40,1)#Start Scope State Machine
        #Get ready signal to read out scope data
        self.xem.UpdateWireOuts()
        ready = bit_chop(self.xem.GetWireOutValue(0x21),ch_select-1, ch_select-1, 32)
        decide_range = 1
        for i in range(num_pulses):
            while ready == 0:
                #print "Stuck"
                self.xem.UpdateWireOuts()
                ready = bit_chop(self.xem.GetWireOutValue(0x21),ch_select-1, ch_select-1, 32)
                #Buff_osc = bytearray(self.scope_samples*4)
                #self.xem.ReadFromPipeOut(ch_select+160, Buff_osc)
                self.xem.ActivateTriggerIn(0x40, 2**(ch_select+3))
                self.xem.ActivateTriggerIn(0x40,1)#Start Scope State Machine

            #self.xem.ActivateTriggerIn(0x40,1)#Start Scope State Machine
            Buff_osc = bytearray(self.scope_samples*4)

            self.xem.ReadFromPipeOut(ch_select+160, Buff_osc)
            Pulse = pipeout_assemble(Buff_osc, 4)
            osc_values = []
            for i in range(len(Pulse)):
                osc_values.append(bit_chop(Pulse[i], 13, 0, 32))
            self.pulse_data.append(osc_values)
            ready = 0
            if plot == 1:
                #Test plotting with real bit file
                if decide_range == 1:
                    maxi = max(osc_values)
                    mini = min(osc_values)
                    decide_range = 0
                self.plot_pulse(osc_values, (maxi+10), (mini-10))
            self.xem.ActivateTriggerIn(0x40, ch_select+3)
        #Set mode back to "stop"
        self.xem.SetWireInValue(0x01, 0, 2**3-1)
        self.xem.UpdateWireIns()
        print "Scope Measurement Complete"
        return Pulse

    def plot_pulse(self, pulse_data, max, min):
        plt.ion()
        #fig = plt.figure()

        self.ax.set_ylim(min, max)
        self.ax.set_xlim(0, len(pulse_data))
        self.line1.set_xdata(range(len(pulse_data)))
        self.line1.set_ydata(pulse_data)
        #line1, = ax.plot( range(len(pulse_data)), pulse_data)


        self.make_figure.canvas.draw()

        plt.pause(0.005)

        return None
