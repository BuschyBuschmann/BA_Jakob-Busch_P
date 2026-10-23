#author: f_scheiber
#%% Imports
import os
import datetime
import time



import libraries.lib.MAIv2Win32.maiv2 as m
from libraries import isel_traverse as isel, goldammer_card as goc

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.transforms import Bbox
import numpy as np
import scipy.signal as sig
import pandas as pd

mpl.use('Qt5Agg')

#%% Setup

# Measurement
folder = '09_windoff_AoA_0_d_1.5mm'
n = 60
t_measure = 60.
window = 'boxcar'
segments = 4000
n_collect = t_measure / 5

# Movement (Plate)
# Calibration Positions, approx. on plate
pos_1_traverse = [0., 269.6] # in traverse coordinates
pos_2_traverse = [500., 270.6] # in traverse coordinates
x_offset = 61. # x_plate = x_traverse - x_offset

pos_1_plate = [pos_1_traverse[0] - x_offset, pos_1_traverse[1]]
pos_2_plate = [pos_2_traverse[0] - x_offset, pos_2_traverse[1]]

# Important Positions:
# x_plate = -50     - mirror start
# x_plate = 262     - mirror end
# x_plate ~= -20    - tripping

x_start_plate = -45.
x_end_plate = 250.
xs_plate = np.linspace(x_start_plate, x_end_plate, n, endpoint=True)
xs_traverse = xs_plate + x_offset

u_infty = 15. #m/s
nu = 1.52e-5 #m^2 / s
l_LE = 300. # mm; length of leading edge

d_99_blasius = lambda x0: 5.29 * np.sqrt(nu * x0/1000 / u_infty) * 1000. # x0 in mm, d_99 in mm
y_TSP = 125e-3

y_pos_plate = lambda x_plate: pos_1_plate[1] + (x_plate-pos_1_plate[0]) * (pos_2_plate[1] - pos_1_plate[1])/(pos_2_plate[0] - pos_1_plate[0])
#y_offset_plate = lambda x_plate: d_99_blasius(x_plate + l_LE) / 2 + y_TSP
y_offset_plate = lambda x_plate: 1.5

x_step = xs_plate[1]-xs_plate[0]
ys = np.array([y_pos_plate(x_plate) + y_offset_plate(x_plate) for x_plate in xs_plate])

# AD-Card
card_hash = 30555830
fs = 192000
block_size = 10000
gain_20db=True
gain_x=m.enumGain.x8

# Isel-Controller
com_port = 'COM4'
baud_rate = 19200

# Plot
fmin, fmax = 10000, 90000
amin, amax = 0., 100.
threshhold = 10000 #to decide if garbage data has been detected

# Wait time before first measurement
t_wait = 600.0

# Output
#plotname = 'psd'
#dfname = 'psd'

#%% Machinery

os.makedirs(os.path.join('messdaten', folder), exist_ok = True)

# AD-Card
siconn = goc.GoldammerCard(card_hash=card_hash, sample_rate=fs)
siconn.AD_ChannelList[0].update_properties(IEPE=False, b_gain=gain_20db, gain=gain_x, highpass=False)
factor = 1
#factor *= 2**gain_x
#if gain_20db:
#    factor *= 100

# Isel-Controller
x_axis = isel.Isel_Axis(name = 'x', steps_per_rev = 400, steigung = 2.5, max_pos = 590.) # LES 5 short
y_axis = isel.Isel_Axis(name = 'y', steps_per_rev = 400, steigung = 2.5, max_pos = 375.) # LES 4 long
x_axis.update_properties(speed = 5)
y_axis.update_properties(speed = 5)
T = isel.Isel_Controller(com_port = com_port, baud_rate = baud_rate, data_bits = 8, axes = [x_axis, y_axis])
T.open()
T.home_axes(['x', 'y'])

#%% Measurements
if t_wait > 0:
    print(f'Waiting for everybody to leave...')
while t_wait > 0:
    print(f'{t_wait:.0f} s remaining...', end='\r')
    time.sleep(1.)
    t_wait -=1

# setup loop
filenames = []
data = np.zeros(int(t_measure * fs))

n_per_segment = np.floor(data.size / segments).astype(int)
freq, _ = sig.welch(data, fs, window=window, nperseg=n_per_segment, noverlap=0)
# setup live plot
plt.ion()
ifmin, ifmax = np.argmin(np.abs(freq-fmin)), np.argmin(np.abs(freq-fmax))
figure1, ((ax1, ax2, ax5), (ax3, ax4, ax6)) = plt.subplots(2, 3, figsize=(10, 10))
#figure1.canvas.manager.window.showMaximized()
cplotlbl1 = 'Displacement FFT Amplitude'
cplotlbl2 = 'Velocity FFT Amplitude'
cplotlbl3 = 'Velocity PSD Amplitude'

def refresh_plots(x_p=None, y=None, both = True):
    if both:
        ax1.clear()
        ax1.set_title('FFT Displacement from PSD')
        ax1.set_xlabel('position in x [mm]')
        ax1.set_ylabel('frequency [Hz]')

        ax3.clear()
        ax3.set_title('FFT Velocity from PSD')
        ax3.set_xlabel('position in x [mm]')
        ax3.set_ylabel('frequency [Hz]')

        ax4.clear()
        ax4.set_title('PSD Velocity')
        ax4.set_xlabel('position in x [mm]')
        ax4.set_ylabel('frequency [Hz]')

        ax6.clear()
        ax6.set_title(f'Summed PSD from {fmin} Hz to {fmax} Hz')
        ax6.set_xlabel('position in x [mm]')
        ax6.set_ylabel('velocity PSD amplitude')

        ax5.clear()
        ax5.set_title('Last Measurement')
        ax5.set_xlabel('frequency [Hz]')
        ax5.set_ylabel('velocity PSD amplitude')
        ax5.set_xlim(left=0, right=fs / 2)
        ax5.grid()

    ax2.clear()
    if x_p is not None and y is not None:
        ax2.set_title(f'Last Measurement\nx = {x_p:.2f} mm, y = {y:.2f} mm')
    else:
        ax2.set_title('Last Block Measurement')
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('Amplitude FFT [mm]')
    ax2.set_xlim(left=0, right=fs / 2)

refresh_plots()
figure1.tight_layout()
figure1.canvas.draw()
plt.show()

df_psd_vel = pd.DataFrame({'freq': freq.tolist()})
df_fft_disp = pd.DataFrame({'freq': freq.tolist()})
df_fft_vel = pd.DataFrame({'freq': freq.tolist()})

xs_plot = np.asarray([x_start_plate - x_step / 2] + [x_plate + x_step / 2 for x_plate in xs_plate])

timedata = None
cbar = None
garbo_runs = 0

#measurement loop
for i, (x_t, x_p, y) in enumerate(zip(xs_traverse, xs_plate, ys)):
    # move to position
    T.move(['x'], [x_t], movement='abs', round_steps = True)
    T.move(['y'], [y], movement='abs', round_steps = True)
    time.sleep(2) # wait for structural vibrations from moving to subside
    for block in range(int(t_measure / n_collect)):
        # garbage until proven good data
        i_lower = int(block * n_collect * fs)
        i_upper = int((block + 1) * n_collect * fs)
        print()
        print(f'Measurement {(i + 1):02d}/{n} block {block + 1}/{int(t_measure / n_collect)}')
        garb_detect = True
        while garb_detect:
            # record data
            siconn.start_measuring(channel_IDs=[0], sample_rate=fs)
            data_raw = siconn.collect_data(n = int(n_collect * fs), blocksize = block_size, ignore_first=10000).reshape((int(n_collect * fs),))
            siconn.stop_measuring()
            #multiply by 10^7 to avoid running into quantization issues in Python.
            data_raw = data_raw * 1e7
            # sanity check whether data was correctly recorded:
            # last 100 values of fft should be near enough 0, as the vibrometer only samples with 50kHz.
            # If not repeat the measurement.
            test_freq, test_psd = sig.welch(data_raw, fs, window=window, nperseg=int(len(data_raw)/10), noverlap=0)
            test_ifmin, test_ifmax = np.argmin(np.abs(test_freq - fmin)), np.argmin(np.abs(test_freq - fmax))
            refresh_plots(x_p=x_p, y=y, both=False)
            ax2.loglog(test_freq, test_psd)
            ax2.plot([0, max(test_freq)], [threshhold*factor, threshhold*factor], 'r-')
            #ax2.set_ylim(top = max(test_psd[test_ifmin:test_ifmax]))
            figure1.canvas.draw()
            figure1.tight_layout()
            figure1.canvas.flush_events()
            if np.mean(test_psd[-100:]) < threshhold*factor:
                garb_detect = False
            else:
                print()
                print(f'Repeating measurement {i+1} block {block + 1} due to bad data!')
                garbo_runs += 1

        data[i_lower : i_upper] = data_raw

    # divide out the measurement gain set in AD-card
    data /= factor

    # write data to file
    dtime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file = f'{dtime}_{i:003d}_x_{x_p:003.5f}_y_{y:003.5f}.csv'
    path = os.path.join('messdaten', folder, file)
    with open(path, 'w') as f:
        data.tofile(f, sep='\n')
    filenames.append(path)

    #calculate psd and fft
    n_per_segment = np.floor(data.size / segments).astype(int)
    _ , avg_psd = sig.welch(data, fs, window=window, nperseg=n_per_segment, noverlap=0)

    df_psd_vel[str(x_p)] = avg_psd
    df_fft_vel[str(x_p)] = np.sqrt(avg_psd) * 2 * freq[1]
    df_fft_disp[str(x_p)] = np.sqrt(avg_psd) / freq / np.pi* freq[1]

    refresh_plots(x_p=x_p, y=y, both=True)
    ax2.loglog(freq, np.abs(avg_psd))
    ax2.set_ylim(top=max(avg_psd[ifmin:ifmax]))

    colorplot1 = ax1.pcolormesh(xs_plot[:i+2], freq[ifmin:ifmax],
                                df_fft_disp.loc[ifmin:ifmax - 1, df_fft_disp.columns != 'freq'].to_numpy()[
                                   1:, :], )  # vmin=amin,vmax=amax, )
    colorplot2 = ax3.pcolormesh(xs_plot[:i+2], freq[ifmin:ifmax],
                                df_fft_vel.loc[ifmin:ifmax - 1, df_fft_vel.columns != 'freq'].to_numpy()[
                                    1:, :], )  # vmin=amin,vmax=amax, )
    colorplot3 = ax4.pcolormesh(xs_plot[:i+2], freq[ifmin:ifmax],
                                df_psd_vel.loc[ifmin:ifmax - 1, df_psd_vel.columns != 'freq'].to_numpy()[
                                    1:, :], )  # vmin=amin,vmax=amax, )
    if i == 0:
        cbar1 = plt.colorbar(colorplot1, label=cplotlbl1)
        cbar2 = plt.colorbar(colorplot2, label=cplotlbl2)
        cbar3 = plt.colorbar(colorplot3, label=cplotlbl3)

    ax6.semilogy(xs_plate[:i+1], np.sum(df_psd_vel.loc[ifmin:ifmax - 1, df_psd_vel.columns != 'freq'].to_numpy(), axis=1))

    figure1.canvas.draw()
    figure1.tight_layout()
    figure1.canvas.flush_events()

    dtime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    for file in os.scandir(f'messdaten/{folder}'):
        if file.name.endswith(".png") and not ('final' in file.name):
            os.unlink(file.path)

    extent = Bbox.union([figure1.axes[0].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted()),
                         figure1.axes[4].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted())])
    figure1.savefig(f'messdaten/{folder}/{folder}_fft_disp_{dtime}_.png', bbox_inches=extent, dpi=300)

    extent = Bbox.union([figure1.axes[2].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted()),
                         figure1.axes[5].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted())])
    figure1.savefig(f'messdaten/{folder}/{folder}_fft_vel_{dtime}_.png', bbox_inches=extent, dpi=300)

    extent = Bbox.union([figure1.axes[3].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted()),
                         figure1.axes[6].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted())])
    figure1.savefig(f'messdaten/{folder}/{folder}_psd_vel_{dtime}_.png', bbox_inches=extent, dpi=300)

plt.ioff()
#%% Measurement End

print('done')
print(f'Number of repeated runs: {garbo_runs}')
##T.close()

dtime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
df_psd_vel.to_csv(f'messdaten/{folder}/{folder}_psd_vel_{dtime}.csv')
df_fft_vel.to_csv(f'messdaten/{folder}/{folder}_fft_vel_{dtime}.csv')
df_fft_disp.to_csv(f'messdaten/{folder}/{folder}_fft_disp_{dtime}.csv')

for file in os.scandir(f'messdaten/{folder}'):
    if file.name.endswith(".png") and not ('final' in file.name):
        os.unlink(file.path)

extent = Bbox.union([figure1.axes[0].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted()),
                     figure1.axes[4].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted())])
figure1.savefig(f'messdaten/{folder}/{folder}_final_fft_disp_{dtime}_.png', bbox_inches=extent, dpi=300)

extent = Bbox.union([figure1.axes[2].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted()),
                     figure1.axes[5].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted())])
figure1.savefig(f'messdaten/{folder}/{folder}_final_fft_vel_{dtime}_.png', bbox_inches=extent, dpi=300)

extent = Bbox.union([figure1.axes[3].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted()),
                     figure1.axes[6].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted())])
figure1.savefig(f'messdaten/{folder}/{folder}_final_psd_vel_{dtime}_.png', bbox_inches=extent, dpi=300)

extent = Bbox.union([figure1.axes[7].get_tightbbox().transformed(figure1.dpi_scale_trans.inverted())])
figure1.savefig(f'messdaten/{folder}/{folder}_final_psd_vel_summed_{dtime}_.png', bbox_inches=extent, dpi=300)