"""
Opal Kelly Functions List
Functions to interface with Opal Kelly API.

WARNING: Some functions may require Opal Kelly FPGA device to be connected to the PC running
the software to properly test. This also requires the "ok" package to be imported from Opal Kelly.
An error will occur if the appropriate package is not imported.

"""
import ok
from tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from ok_analysis import *
import csv
import os
from osu_rad_settings import settings_update

class RadDevice(object):
    """
    Class to designate FPGA systems at Oregon State University to connect them
    via the USB.
    """

    def __init__(self):
        pass

    def program_device(self):
        """
        program_device:
        Simple function to create an object of the connected FPGA device. Opens
        Tkinter window for user to select Bit_File to program the FPGA. The window
        then closes and programs the FPGA. Also checks for errors.
        """
        self.xem = ok.okCFrontPanel()
        self.xem.OpenBySerial("")
        root = Tk()
        root.update()
        Bit_File = askopenfilename()
        root.update()
        root.destroy()
        error = self.xem.ConfigureFPGA(str(Bit_File))
        if error != 0:
            print "Error Connecting!"
            sys.exit()
        else:
            print "FPGA Connect and Programmed!"
        return None

    def update_settings_file(self, ch_num = 1, trig_thres = 200,
     flat_time = 3, peak_time = 12, peak_gain = 0,
     flat_gain = 0, conversion_gain = 2):
        """Updates example settings file to change specified settings from any channel number. Must be run
        multiple times if other parameters need to be updated for other channels.
        """
        settings = [ch_num, trig_thres, flat_time, peak_time, peak_gain, flat_gain, conversion_gain]

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

    def manual_wirein(self, address, value):
        self.xem.SetWireInValue(address,value, 2**32-1)
        self.xem.UpdateWireIns()

    def pipeout_read(self, address, bytes):
        Data_Buffer = bytearray('\x00'*bytes*4)#Assuming OK 4 byte read
        self.xem.ReadFromPipeOut(address, Data_Buffer)
        return Data_Buffer
