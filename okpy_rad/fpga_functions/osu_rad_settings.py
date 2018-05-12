"""
Python script to write the update setting file for the auot_update_settings method
describe din the RadDevice class. When settings need to be updated, this script
should also be updated with the desired settings.
"""
import csv


def settings_update(Settings, **kwargs):
    """
    Settings Update will update the FPGA using a single settings variable.
    Each item in the Settings list is a specific variable
    ###########################
    Index |  Settings Variable
    [0]   |  Channel Number
    [1]   |  Trigger Threshold
    [2]   |  Flat Time
    [3]   |  Peaking Time
    [4]   |  Trapezoid Peak Gain
    [5]   |  Trapezoid Flat Gain
    [6]   |  Conversion Gain
    """

    Data_Write = [] #Create list for all wire data



    Ch_Num = Settings[0] - 1
    run_mode = 0
    gate = 0; # 0 = off, 1 = on
    time_mode = 0; # 0 = real, 1 = live
    pileup = 0; # 0 = off, 1 = on
    #xem.UpdateWireIns()
    peaking_gain = 0; # 0-3; mult x1, x2, x4, x8
    flat_gain = 0;    # 0-3; mult x1, x2, x4, x8
    trap_gain = peaking_gain + flat_gain*2**2;


    ep01wire = run_mode + gate*(2**3) + time_mode*(2**5) + pileup*(2**6) + trap_gain*(2**10);
    Data_Write.append([0x01, ep01wire, 0])


    #Trigger threshold section
    trigger_thresholds = [200,200,200,200,200,200,200,200] # max 65335
    trigger_thresholds[Ch_Num] = Settings[1]
    ep02wire = trigger_thresholds[0] + trigger_thresholds[1]*(2**16)
    ep03wire = trigger_thresholds[2] + trigger_thresholds[3]*(2**16)
    ep04wire = trigger_thresholds[4] + trigger_thresholds[5]*(2**16)
    ep05wire = trigger_thresholds[6] + trigger_thresholds[7]*(2**16)
    Data_Write.append([0x02, ep02wire, 0])
    Data_Write.append([0x03, ep03wire, 0])
    Data_Write.append([0x04, ep04wire, 0])
    Data_Write.append([0x05, ep05wire, 0])

    #xem.UpdateWireIns()
    #Trapezoidal filter section
    trap_peak = [12,12,12,12,12,12,12,12]
    trap_peak[Ch_Num] = Settings[3]
    trap_flat = [3,3,3,3,3,3,3,3]
    trap_flat[Ch_Num] = Settings[2]

    #Shaping parameters
    shaping_pars =\
       [trap_peak[0]+trap_flat[0]*(2**4),trap_peak[1]+trap_flat[1]*(2**4),\
       trap_peak[2]+trap_flat[2]*(2**4),trap_peak[3]+trap_flat[3]*(2**4),\
       trap_peak[4]+trap_flat[4]*(2**4),trap_peak[5]+trap_flat[5]*(2**4),\
       trap_peak[6]+trap_flat[6]*(2**4),trap_peak[7]+trap_flat[7]*(2**4)]
    ep06wire = shaping_pars[0] + shaping_pars[1]*(2**8)\
       + shaping_pars[2]*(2**16) + shaping_pars[3]*(2**24);
    ep07wire = shaping_pars[4] + shaping_pars[5]*(2**8)\
       + shaping_pars[6]*(2**16) + shaping_pars[7]*(2**24);

    Data_Write.append([0x06, ep06wire, 0])
    Data_Write.append([0x07, ep07wire, 0])


    peaking_gain = Settings[4]; # 0-3; mult x1, x2, x4, x8
    flat_gain = Settings[5];    # 0-3; mult x1, x2, x4, x8
    trap_gain = peaking_gain + flat_gain*2**2
    Data_Write.append([0x00, trap_gain*(2**10), 2*32-1])


    mca_time = 100; # in s, down to ~0.01s
    ct_lsb = 2**17*8E-9; # position of time inside FPGA * sys_clk period in sec
    collection_time = int(round(mca_time/ct_lsb));
    ep08wire = collection_time;
    # xem.SetWireInValue(0x08,ep08wire,2**32-1);
    Data_Write.append([0x08, ep08wire, 0])
    conversion_gains = [2,2,2,2,2,2,2,2]; # range 0-15
    conversion_gains[Ch_Num] = Settings[6]
    ep09wire = conversion_gains[0] + conversion_gains[1]*(2**4)\
        + conversion_gains[2]*(2**8) + conversion_gains[3]*(2**12)\
        + conversion_gains[4]*(2**16) + conversion_gains[5]*(2**20)\
        + conversion_gains[6]*(2**24) + conversion_gains[7]*(2**28);
    #xem.SetWireInValue(0x09,ep09wire,2**32-1);
    # xem.UpdateWireIns()
    Data_Write.append([0x09, ep09wire, 0])
    Data_Write.append([0x40, 3, 1])


    with open('settings.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter= ',')
        for item in Data_Write:
            spamwriter.writerow(item)

    return None