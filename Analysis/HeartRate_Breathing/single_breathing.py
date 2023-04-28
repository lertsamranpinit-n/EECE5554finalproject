from bagpy import bagreader
import pandas as pd
import seaborn as sea
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import math
import csv
from scipy.signal import butter, filtfilt
from scipy.signal import iirnotch, filtfilt
from scipy.signal import find_peaks

def remove_first_x_elements(arr, x):
     return arr[x:]

def remove_last_x_elements(arr, x):
    return arr[:-x] if x > 0 else arr

Immanuel_heart = bagreader('Immanuel_Heart.bag')
Jason_heart = bagreader('Jason_heart.bag')
Jasmine_heart = bagreader('jasmin_breathing.bag')
June_heart = bagreader('june_breathing.bag')
Note_heart = bagreader('note_breathing.bag')
Immanuel_breathing = bagreader('Immanuel_Breathing.bag')
csvfiles = []

for t in Jasmine_heart.topics:
    data1 = Jasmine_heart.message_by_topic(t)
    csvfiles.append(data1)

for t in Note_heart.topics:
    data3 = Note_heart.message_by_topic(t)
    csvfiles.append(data3)

for t in June_heart.topics:
    data2 = June_heart.message_by_topic(t)
    csvfiles.append(data2)

breathing_df = pd.read_csv('june_breathing/imu.csv')

breathing_message = breathing_df['VNYMR'].values

i = 0
time = breathing_df['Time'].values
time = time - time[0]

accX = []
accY = []
accZ = []

#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------

while i < len(breathing_message):
     accX.append(float(breathing_message[i].split(',')[10]))
     accY.append(float(breathing_message[i].split(',')[11]))
     accZ.append(float((breathing_message[i].split(',')[12]).split('*')[0]))
     i += 1
accX = np.array(accZ)

new_time = remove_first_x_elements(time, int((len(time)/2)))
new_time = new_time - new_time[0]
new_accx = remove_first_x_elements(accX, int((len(time)/2)))

time = remove_last_x_elements(new_time, int(len(new_time)/11))
accX = remove_last_x_elements(new_accx, int(len(new_time)/11))

#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
# Fit a linear line to the data
slope, intercept = np.polyfit(time, accX, 1)

# Evaluate the linear line at each time step
linear_trend = np.polyval([slope, intercept], time)

# Remove the linear trend from the acceleration data
detrended_accX = accX - linear_trend

#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
# Apply a 12-28 Hz IIR Butterworth bandpass filter
low_frequency = 0.17
high_frequency = .33
nyquist_frequency = 0.5 * 40
low_cutoff = low_frequency / nyquist_frequency
high_cutoff = high_frequency / nyquist_frequency
order = 2

b, a = butter(order, [low_cutoff, high_cutoff], btype='band')
# Apply the filter to the acceleration data using filtfilt (forward and reverse filtering)
filtered_acc = filtfilt(b, a, detrended_accX)

#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
# Take the absolute value of the filtered signal
abs_filtered_acc = np.maximum(filtered_acc, 0)

# Find the peaks
peak_indices, _ = find_peaks(abs_filtered_acc)

# Count the peaks
peak_count = len(peak_indices)
seconds = time[len(time)-1]
print("Number of peaks:", peak_count)
print(seconds)
bpm = 60*(peak_count/seconds)

Immanuel_res = abs_filtered_acc
print(bpm)
# Create a 3x1 grid of plots
fig, axes = plt.subplots(3, 1, figsize=(10, 10))

axes[0].plot(time, detrended_accX, label = "Subject 1 Raw ACCZ")
axes[0].set_xlim(0, 120)
axes[0].set_xlabel('Time[sec]')
axes[0].set_ylabel('Acceleration [m/sec2]')
axes[0].set_title('Raw Diaphragm Acceleration Data')
axes[0].legend()

axes[1].plot(time, filtered_acc, label = 'Subject 1: 14 Breaths per minute')
axes[1].set_xlim(0, 120)
axes[1].set_xlabel('Time[sec]')
axes[1].set_ylabel('Acceleration [m/sec2]')
axes[1].set_title('IIR Bandpass Filtered Breathing')
axes[1].legend()

axes[2].plot(time, Immanuel_res, label = 'Subject 1: 16 Breaths per minute')
axes[2].set_xlim(0, 120)
axes[2].set_xlabel('Time[sec]')
axes[2].set_ylabel('Acceleration [m/sec2]')
axes[2].set_title('Extracted Peaks')
axes[2].legend()

# Add some space between the subplots
plt.subplots_adjust(hspace=0.8)

plt.show()