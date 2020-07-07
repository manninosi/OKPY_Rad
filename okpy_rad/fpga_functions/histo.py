from .ok_funcs import RadDevice
from .ok_analysis import *
import numpy as np
import matplotlib.pyplot as plt

class HistoMode(RadDevice):
    """

    """

    def __init__(self, run_mode = 2):
        self.run_mode = run_mode
        self.mca_data = []
        self.data_acquired = 0
        self.peak_ind = []
        #Making plotting object
        self.make_figure = plt.figure()
        self.ax = self.make_figure.add_subplot(111)#Creates figure object
        self.line1, = self.ax.plot([],  [])

    def start_mca(self,  ch_select = 1, plot = 1):
        """Method to run MCA for FPGA and acquire all data

        Plot(bool):
            True : Will update gamma spectrum as data is being data acquired
            False: No plotting will occur

        The ActivateTriggerIn addresses are currently hard coded in and should be
        manually changed if a user creates specific VHDL file. Status_out keeps
        track if the MCA state machine is completed and also has a hard coded
        address.
        """
        #MCA_done = 0
        #Set FPGA to MCA mode
        ep01wire = self.run_mode
        self.xem.SetWireInValue(0x01, ep01wire, 2**3-1)
        self.xem.UpdateWireIns()
        Data = []
        if self.run_mode == 2:
            self.xem.ActivateTriggerIn(0x41, 1) #Host Reset
            self.xem.ActivateTriggerIn(0x40, 1) #Start Trigger for State machine
            self.xem.UpdateWireOuts()
            status_out = self.xem.GetWireOutValue(0x21)
            MCA_done = bit_chop(status_out, ch_select +7, ch_select+7, 32)
            while MCA_done != 1:
                self.xem.UpdateWireOuts()
                status_out =self.xem.GetWireOutValue(0x21)
                MCA_done = bit_chop(status_out, ch_select+7, ch_select+7, 32)
                #print bin(bit_chop(status_out, 31, 0, 32))[2:]
                Buf_Data = bytearray(4096*4)
                self.xem.ReadFromPipeOut(ch_select+176, Buf_Data)
                self.mca_data = pipeout_assemble(Buf_Data, 4)
                Data.append(self.mca_data)
                self.xem.ActivateTriggerIn(0x41, 2)#Update Times
                if plot == 1:
                    #print "Updating Gamma Spectrum"
                    self.plot_mca(self.mca_data)
            self.data_acquired = 1
        else:
            print( "Run Mode is not set to 2 for MCA")#MCA run mode is 2
            #Consider adding function to change mode
        print( "Histogram Run Complete.")
        return Data

    def plot_mca(self, data):
        """Takes in MCA_data and plots the spectrum
        """
        plt.ion()
        self.ax.set_ylim(min(data) - 10, max(data) + 10)
        self.ax.set_xlim(left = -10, right = 6000)
        self.line1.set_xdata(range(len(data)))
        self.line1.set_ydata(data)
        self.make_figure.canvas.draw()
        plt.pause(0.005)

    def find_peaks(self, mph=None, mpd=1, threshold=100, edge='rising', kpsh=False, valley=False, show=False, ax=None):
        """Finds indices of maximum for all peaks that exceed the set threshold
        """
        if self.data_acquired == 0:
            print("Acquire MCA data before finding peaks")
            return None
        else:
            self.peak_ind =  detect_peaks(self.mca_data, mph=mph, mpd=mpd, threshold=threshold, edge=edge, kpsh=kpsh, valley=valley, show=show, ax=ax)
            return self.peak_ind


    def get_calibration(self):
        if self.data_acquired == 0:
            print("Acquire MCA data before conducting calibration")
        else:
            print("There are %3.0f peaks that exceeded the threshold"%(len(self.peak_ind)))
            Cal_Check = 'Y'
            Energies = []
            Cal_Points = []
            points = []
            Counter = 0
            while Cal_Check == 'Y' and Counter < len(self.peak_ind):
                Keep_Point = str(raw_input('Keep peak %2.0f? (Check Spectrum)' %(Counter+1)))
                while Keep_Point != 'Y' and Keep_Point != 'N':
                    Keep_Point = raw_input('Wrong input, please only use Y or N')
                if Keep_Point == 'Y':
                    Cal_Points.append(self.peak_ind[Counter])
                    Energies.append(raw_input('Entery Energy of peak in KeV: '))
                Counter += 1
                Cal_Check = raw_input('keep calibrating peaks? (Y/N)')
                while  Cal_Check != 'Y' and Cal_Check != 'N':
                    Cal_Check = raw_input('Wrong input, please only use Y or N')
            #Form cal points and energies into a tpble
            for i in range(len(Cal_Points)):
                    points.append(tuple([Cal_Points[i], Energies[i]]))
            #Zip points together to solve for slope and intersect
            x_coords, y_coords = zip(*points)
            A = np.vstack([x_coords,np.ones(len(x_coords))]).T
            m, c = np.linalg.lstsq(A, y_coords)[0]
            print("Line Solution is y = {m}x + {c}".format(m=m,c=c))

            Save_Q = raw_input("Save solution as pickle? (Y/N)")
            if Save_Q == 'Y':
                SaveName = asksaveasfilename()
                Data = [m,c]
                File = open(SaveName, 'wb')
                pickle.dump(Data, File)
                File.close()
        return m, c
