from okpy_rad.fpga_functions.ok_funcs import *
from okpy_rad.fpga_functions.scope    import *

device = ScopeMode()#Create

device.program_device()
device.auto_wirein()
device.update_settings_file()
device.get_pulse_data()
