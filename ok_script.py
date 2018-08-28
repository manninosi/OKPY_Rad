from okpy_rad.fpga_functions.ok_funcs import *
from okpy_rad.fpga_functions.scope    import *
from okpy_rad.fpga_functions.histo    import *
from okpy_rad.fpga_functions.listo    import *
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_pdf import PdfPages
import csv
#pp = PdfPages('multipage.pdf')


# device = ScopeMode()#Create scope object
#
# device.program_device()
# device.update_settings_file( ch_num = [5], trig_thres = [200],
#  flat_time = [3], peak_time = [12], peak_gain = 0,
#  flat_gain = 0, conversion_gain = [7], MCA_Time = 60, pol = '00000101',
#  coin_window = 100, data_delay = 400, rec_sing = 0)
# # device.auto_wirein()
# device.auto_wirein()
# device.update_settings_file()
# pulse_data = device.get_pulse_data(ch_select = 5, num_pulses=500, plot=1)

# fig = plt.figure()
# ax = plt.subplot(111)
# ax.spines["top"].set_visible(False)
# ax.spines["bottom"].set_visible(False)
# ax.spines["right"].set_visible(False)
# ax.spines["left"].set_visible(False)
# ax.grid(linestyle= ':')
# line, = ax.plot([], [], lw=2)
# ax.set_ylim(min(pulse_data[0])-20, max(pulse_data[0])+20)
# ax.set_xlim(0, len(pulse_data[0])*8)
# ax.set_xlabel('Time(us)')
# ax.set_ylabel('ADC Value(14-bit)')
# ax.set_title('Scope Module')
#
# def init():
#     line.set_data([], [])
#     return line,
#
# def animate(i, data):
#     x = np.array(range(len(data[i])))*8/100
#     y = data[i]
#
#     line.set_data(x,y)
#     return line,
#
# anim = animation.FuncAnimation(fig, animate, init_func=init, fargs = [pulse_data],
#                                frames = len(pulse_data), interval=50, blit=True)
#
# anim.save('scope_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
#
# plt.show()
# print "finished"


"""
HISTOGRAM SCRIPT WITH ANIMATION
"""



# device = HistoMode() #Create histogram object
# device.program_device()
#
# device.update_settings_file( ch_num = [5], trig_thres = [200],
#  flat_time = [3], peak_time = [12], peak_gain = 0,
#  flat_gain = 0, conversion_gain = [10], MCA_Time = 60, pol = '00000101',
#  coin_window = 100, data_delay = 400, rec_sing = 0)
# device.auto_wirein()
#
# pulse_data = device.start_mca(ch_select = 5)
# indices = device.find_peaks(mph = 2000, threshold=0, mpd = 20)
# print indices
# #m,b = device.get_calibration()
#
#
#
# fig = plt.figure()
# ax = plt.subplot(111)
# ax.spines["top"].set_visible(False)
# ax.spines["bottom"].set_visible(False)
# ax.spines["right"].set_visible(False)
# ax.spines["left"].set_visible(False)
#
# ax.plot(range(len(pulse_data[-1])), pulse_data[-1], lw=2)
# values = [pulse_data[-1][i] for i in indices] #Grab values from last MCA_data
# thres_line = [2000 for i in range(len(pulse_data[-1]))]
# ax.plot(indices, values, 'o', markersize = 8, fillstyle = 'none') #Points where peaks occur
# ax.plot(range(len(pulse_data[-1])), thres_line, ':', color = 'r')#Threshold line
# ax.set_ylim(min(pulse_data[0]), max(pulse_data[-1])+200)
# ax.set_xlim(0, len(pulse_data[0])+100)
# ax.set_xlabel('Channel Number')
# ax.set_ylabel('Counts')
# ax.set_title('Histogram Module')
#
# plt.savefig(pp, format='pdf')
# pp.close()


# def init():
#     line.set_data([], [])
#     return line,

#
# def animate(i, data):
#     x = np.array(range(len(data[i])))
#     y = data[i]
#
#     line.set_data(x,y)
#     return line,
#
# anim = animation.FuncAnimation(fig, animate, init_func=init, fargs = [pulse_data],
#                                frames = len(pulse_data), interval=100, blit=True)
#
# anim.save('histo_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
#
# plt.show()


"""
LISTOGRAM SCRIPT
"""


device = ListoMode() #Create histogram object
device.program_device()

device.update_settings_file( ch_num = [5], trig_thres = [200],
 flat_time = [3], peak_time = [12], peak_gain = 0,
 flat_gain = 0, conversion_gain = [10], MCA_Time = 60, pol = '00000101',
 coin_window = 100, data_delay = 400, rec_sing = 0)
device.auto_wirein()
device.set_intervals(intvl = 15, cycle = 225)
list_data = device.run_listo(ch_select = 5)
file_name = "Drift_Data_20180619_8intvl_30min_Larger_Offset"
with open(file_name, 'wb') as csvfile:
    Writer = csv.writer(csvfile, delimiter = ',')
    for i in range(len(list_data)):
        Writer.writerow(list_data[i])
#
#
# coarsen_data = device.coarsen_listo_data(list_data)
#device.plot_listo_data(coarsen_data, save_pdf = 1)
