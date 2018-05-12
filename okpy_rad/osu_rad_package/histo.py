from ..fpga_functions.ok_funcs import RadDevice


class McaHisto(RadDevice):
    def __init__(self, run_mode = 2):
        self.run_mode = run_mode
        self.mca_data = []
        self.data_acquired = 0

    def change_run_md(self, address = 1):
        self.xem.SetWiteInValue(self.run_mode, 2**32-1)
        self.xem.UpdateWireIns()

    def run_mca(self, time, time_sel = 0, plot = 0):
        """Method to run MCA for FPGA and acquire all data
        """
        MCA_done = 0
        if self.run_mode == 2:
            if time_sel == 1: #real time_sel
                return None
                if plot == 1:
                    pass
                    #Print the data as it streams in
            else: #Live Time
                pass
                if plot == 1:
                    pass
                    #Print the data as it streams in
                return None
        else:
            print "Run Mode is not set to 2 for this mode"#MCA run mode is 2
            #Consider adding function to change mode
    def plot_mca(self):
        pass

    def find_peaks(self):
        if self.data_acquired == 0:
            print "Acquire MCA data before finding peaks"
        else:
            pass
            #Find peaks
    def get_calibration(self):
        pass
        #Use peak finding to generate calibration
