from okpy_rad.fpga_functions.ok_funcs import *
from okpy_rad.fpga_functions.scope    import *
from okpy_rad.fpga_functions.histo    import *

device = ScopeMode()#Create scope object

device.program_device()
device.update_settings_file( ch_num = [5], trig_thres = [200],
 flat_time = [3], peak_time = [12], peak_gain = 0,
 flat_gain = 0, conversion_gain = [7], MCA_Time = 60, pol = '00000101',
 coin_window = 100, data_delay = 400, rec_sing = 0)
# device.auto_wirein()
device.auto_wirein()
device.update_settings_file()
device.get_pulse_data(ch_select = 5)


# device = HistoMode() #Create histogram object
# device.program_device()
#
# device.update_settings_file( ch_num = [5], trig_thres = [200],
#  flat_time = [3], peak_time = [12], peak_gain = 0,
#  flat_gain = 0, conversion_gain = [7], MCA_Time = 60, pol = '00000101',
#  coin_window = 100, data_delay = 400, rec_sing = 0)
# device.auto_wirein()
#
# device.start_mca(ch_select = 5)
