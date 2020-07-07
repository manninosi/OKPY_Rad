"""
Opal Kelly Functions List
Functions to interface with Opal Kelly API.

WARNING: Some functions may require Opal Kelly FPGA device to be connected to the PC running
the software to properly test. This also requires the "ok" package to be imported from Opal Kelly.
An error will occur if the appropriate package is not imported.

"""
import ok
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
#from tkFileDialog import askopenfilename, asksaveasfilename
from .ok_analysis import *
import csv
import os
from .osu_rad_settings import settings_update

class RadDevice(object):
    """Class to connect radiation detection systems with FPGAs via Opal Kelly API.
    """

    def __init__(self, run_mode = 1):
        self.run_mode = run_mode

    def program_device(self):
        """
        program_device:
        Function to create an object of the connected FPGA device. Opens
        Tkinter window for user to select Bit_File to program the FPGA. The window
        then closes and programs the FPGA. Also checks for errors during FPGA
        programming.

        """
        self.xem = ok.okCFrontPanel()
        self.xem.OpenBySerial("")
        root = Tk()
        root.update()
        print("Select Bit File...")
        Bit_File = askopenfilename()
        print(Bit_File)
        root.update()
        root.destroy()
        error = self.xem.ConfigureFPGA(str(Bit_File))
        if error != 0:
            print("Error Connecting!")
            sys.exit()
        else:
            print("FPGA Connect and Programmed!")
        return None

    def update_settings_file(self, ch_num = [1], trig_thres = [200],
     flat_time = [3], peak_time = [12], peak_gain = 0,
     flat_gain = 0, conversion_gain = [2], MCA_Time = 100, pol = '00000101',
     coin_window = 100, data_delay = 400, rec_sing = 0, trig_flat = [3], trig_peak = [12]):
        """Updates example settings file to change specified settings from any channel number. Must be run
        multiple times if other parameters need to be updated for other channels.

        If multiple channels are changed, the corresponding variables need to match length and desired location:
            trig_thres
            flat_time
            peak_time
            conversion_gain
        """
        settings = [ch_num, trig_thres, flat_time, peak_time, peak_gain, flat_gain, conversion_gain, MCA_Time, pol, coin_window,
        data_delay, rec_sing, trig_flat, trig_peak]

        settings_update(settings)
        return None

    def auto_wirein(self):
        """Grabs settings.csv file to update a series of WireIns from
        Opal Kelly. Settings.csv file is described in the README
        """
        file_dir = os.path.join(os.getcwd(), 'settings.csv')
        wire_in = []
        trigger_in = []
        with open(file_dir, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter = ',')
            for row in spamreader:
                if row[-1] == '0':
                    values= (map(int,row))
                    self.xem.SetWireInValue(values[0],values[1],2**32-1)
                    self.xem.UpdateWireIns()
                elif row[-1] == '1':
                    values = (map(int,row))
                    self.xem.ActivateTriggerIn(values[0],values[1])

    def manual_wirein(self, address, value, mask = 2**32-1):
        self.xem.SetWireInValue(address,value, mask)
        self.xem.UpdateWireIns()

    def pipeout_read(self, address, chunks):
        """Conducts Pipe Read from OK and specified address.

        Address(hex or int): Pipe out address
        chunks(int): Number of 32-bit chunks to be read
        """
        Data_Buffer = bytearray('\x00'*chunks*4)#Assuming OK 4 byte read
        self.xem.ReadFromPipeOut(address, Data_Buffer)
        Result = pipeout_assemble(Data_Buffer, 4)
        return Result


    def get_energy(self, data, pkt = 100, flt = 400):
        """Perfroms convolution with a trapezoidal filter
        data(array): Contains raw pulse data
        pkt(int): Peaking time for trapezoidal filter
        flt(int): Flat top time for trapezoidal filter
        """
        filter = np.concatenate((np.ones(pkt), np.zeros(flt), np.ones(pkt)/-1))

    def change_run_mode(self, run_mode):
        """used to manually change the run Mode
        WARNING: Only use if you need to change the run mode to fit your needs.
        """
        self.run_mode = run_mode
        self.xem.SetWiteInValue(0,0x01, self.run_mode, 2**32-1)
        self.xem.UpdateWireIns()
