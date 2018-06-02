from ok_funcs import RadDevice
from ok_analysis import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.backends.backend_pdf import PdfPages


class ListoMode(RadDevice):

    def __init__(self, run_mode = 5):
        self.run_mode = run_mode


        #Making plotting object
        self.make_figure = plt.figure()
        self.ax = self.make_figure.gca(projection='3d')#Creates figure object


    def set_intervals(self, intvl = 1, cycle = 10, address = 0x0C):
        ep0Cwire = intvl + cycle*(2**4)
        self.xem.SetWireInValue(address, ep0Cwire, 2**32-1)
        self.xem.UpdateWireIns()


    def run_listo(self, ch_select = 1):
        """Start to take listogram measurements

        Make sure to run the "set_intervals" method before executing "run_listo"
        """
        #Set FPGA to MCA mode
        ep01wire = self.run_mode
        self.xem.SetWireInValue(0x01, ep01wire, 2**3-1)
        self.xem.UpdateWireIns()

        #Start Listogram statemachine
        self.xem.ActivateTriggerIn(0x40, 1)

        #Checks to see if MCA_done is complete
        self.xem.UpdateWireOuts()
        status_out = self.xem.GetWireOutValue(33)
        MCA_done = bit_chop(status_out,ch_select+7,ch_select+7,32)
        #Array to hold Listogram Data
        listo_data = []
        while MCA_done != 1:

            self.xem.UpdateTriggerOuts()
            #Check to to read BRAM
            start_mca_read = self.xem.IsTriggered(96,2**32-1)

            self.xem.UpdateWireOuts()
            status_out = self.xem.GetWireOutValue(33)
            MCA_done = bit_chop(status_out,ch_select+7,ch_select+7,32)
            count = 1
            if start_mca_read == 1:
                Buf_Data = bytearray(4*4096)
                self.xem.ReadFromPipeOut(176 + ch_select, Buf_Data)
                print sum(pipeout_assemble(Buf_Data,4))
                listo_data.append(pipeout_assemble(Buf_Data,4))
                print "The current interval is: %3.0f" %count
                count += 1
        return listo_data

    def coarsen_listo_data(self, listo_data):
        """Takes in listogram data intervals and will combine set_intervals
        as specified by the user. """
        listo_data = np.array(listo_data)
        print "There are %3.0f intervals in this data" %(len(listo_data))

        self.Interval_Comb = input("Enter the number of seconds to combine listogram data: ")
        self.Interval_Tot = len(listo_data)/self.Interval_Comb #Will determin how many iterations to combine data

        Combined_Data = []
        for i in range(self.Interval_Tot):
            Combined_Data.append(listo_data[i*self.Interval_Comb:(i*self.Interval_Comb)+self.Interval_Comb].sum(axis=0))
        Combined_Data.append(listo_data[i*self.Interval_Comb:(i*self.Interval_Comb)+len(listo_data)%self.Interval_Comb].sum(axis=0))

        return Combined_Data

    def plot_listo_data(self, listo_data, save_pdf = 0):
        Time_Plot = []
        #Create time array for 3D plot
        for i in range(1, 1+self.Interval_Tot):
            Time_Plot.append(self.Interval_Comb*i)

        zs = Time_Plot
        verts = []
        #Create tuples for 3D plot
        for i in range(len(zs)):
            verts.append(list(zip(range(len(listo_data[i])), listo_data[i])))

        poly = LineCollection(verts)
        self.ax.add_collection3d(poly, zs=zs, zdir='y')

        self.ax.set_xlabel('Channel(#)', fontsize = 15)
        self.ax.set_xlim3d(-5, max(range(len(listo_data[0]))) + 5)
        self.ax.set_ylabel('Time(secs)', fontsize = 15)
        self.ax.set_ylim3d(0, max(Time_Plot))
        self.ax.set_zlabel('Counts', fontsize = 15)
        self.ax.set_zlim3d(0,max(listo_data[0]))
        self.ax.set_title("Listogram Data",y = 1.08)
        if save_pdf == 1:
            file_name = input("Enter file name to save PDF image: ")
            pp = PdfPages('multipage.pdf')
            plt.savefig(pp, format='pdf')
            pp.close()
        plt.show()
