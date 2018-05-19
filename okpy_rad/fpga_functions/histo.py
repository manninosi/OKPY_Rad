from ok_funcs import RadDevice
from ok_analysis import *
import numpy as np

class MCAHisto(RadDevice):
    def __init__(self, run_mode = 2):
        self.run_mode = run_mode
        self.mca_data = []
        self.data_acquired = 0
        self.peak_ind = []

    def change_run_md(self, run_mode):
        """used to manually change the run Mode
        WARNING: Only use if you need to change the run mode to fit
        your needs.
        """
        self.run_mode = run_mode
        self.xem.SetWiteInValue(0,01, self.run_mode, 2**32-1)
        self.xem.UpdateWireIns()

    def start_mca(self,  ch_select = 1, plot = 0):
        """Method to run MCA for FPGA and acquire all data

        Plot(1 or 0):
            1: Will update gamma spectrum as data is being data acquired
            0: No plotting will occur

        The ActivateTriggerIn addresses are currently hard coded in and should be
        manually changed if a user creates specific VHDL file. Status_out keeps
        track if the MCA state machine is completed and also has a hard coded
        address.
        """
        MCA_done = 0
        #Set FPGA to MCA mode
        ep01wire = self.run_mode
        self.xem.SetWireInValue(0x01, ep01wire, 2**3-1)

        if self.run_mode == 2:
            self.xem.ActivateTriggerIn(0x41, 1) #Host Reset
            self.xem.ActivateTriggerIn(0x40, 1) #Start Trigger for State machine
            self.xem.UpdateWireOuts()
            status_out = bit_chop(self.xem.GetWireOutValue(0x21)) #Rea
            MCA_done = bit_chop(status_out, ch_select +8, ch_select+8, 32)
            while MCA_done != 1:
                status_out =self.xem.GetWireOutValue(33)
                MCA_done = bit_chop(status_out, ch_select+8, ch_select+8, 32)
                Buf_Data = bytearray('\x00'*4096*4)
                self.xem.ReadFromPipeOut(ch_select+176, Buf_Data)
                self.mca_data = Pipeout_Assemble(Buf_Data, 4)

                if plot == 1:
                    print "Updating Gamma Spectrum"
                    self.plot_mca(self.mca_data)
            self.data_acquired = 1
        else:
            print "Run Mode is not set to 2 for MCA"#MCA run mode is 2
            #Consider adding function to change mode

    def plot_mca(self, data):
        """Takes in MCA_data and plots the spectrum
        """
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        line1, = ax.plot(x,  y)
        ax.set_ylim(min(data) - 10, max(data) + 10)
        ax.set_xlim(left = -10, right = 6000)
        line1.set_xdata(range(len(data)))
        line1.set_ydata(data)
        fig.canvas.draw()
        plt.pause(0.005)

    def find_peaks(self, mph=None, mpd=1, threshold=0, edge='rising', kpsh=False, valley=False, show=False, ax=None):
        """Finds indices of maximum for all peaks that exceed the set threshold
        """
        if self.data_acquired == 0:
            print "Acquire MCA data before finding peaks"
        else:
            self.peak_ind =  detect_peaks(self.mca_data, mph=mph, mpd=mpd, threshold=0, edge=edge, kpsh=kpsh, valley=valley, show=show, ax=ax)


    def get_calibration(self):
        if self.data_acquired == 0:
            print "Acquire MCA data before conducting calibration"
        else:
            Cal_Check == 'Y'
            Energies = []
            Cal_Points = []
            Counter = 0
            while Cal_Check == 'Y' and Counter < len(self.peak_ind):
                Keep_Point = str(raw_input('Keep peak %2.0f? (Check Spectrum)' %(Counter+1))
                while  Keep_Point != 'Y' and Keep_Point != 'N':
                    Keep_Point = raw_input('Wrong input, please only use Y or N')
                if Keep_Point == 'Y':
                    Cal_Points.append(self.peak_ind[Counter])
                    Energies.append(raw_input('Entery Energy of peak in KeV: '))
                Counter += 1
                Cal_Check = raw_input('keep calibrating peaks? (Y/N)')
                while  Cal_Point != 'Y' and Cal_Point != 'N':
                    Cal_Point = raw_input('Wrong input, please only use Y or N')
