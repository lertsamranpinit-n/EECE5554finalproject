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
Jasmine_heart = bagreader('jasmin_heartrate.bag')
June_heart = bagreader('june_heartrate.bag')
Note_heart = bagreader('note_heartrate.bag')
Immanuel_breathing = bagreader('Immanuel_Breathing.bag')
csvfiles = []

for t in Immanuel_heart.topics:
    data1 = Immanuel_heart.message_by_topic(t)
    csvfiles.append(data1)

for t in Note_heart.topics:
    data3 = Note_heart.message_by_topic(t)
    csvfiles.append(data3)

for t in June_heart.topics:
    data2 = June_heart.message_by_topic(t)
    csvfiles.append(data2)

heart_df = pd.read_csv('note_heartrate/imu.csv')
# breathing_df = pd.read_csv('Immanuel_Breathing/imu.csv')

heart_message = heart_df['VNYMR'].values
# breathing_message = breathing_df['VNYMR'].values

i = 0
time = heart_df['Time'].values
time = time - time[0]
print(time[0])

accX = []
accY = []
accZ = []

#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------

while i < len(heart_message):
     accX.append(float(heart_message[i].split(',')[7]))
     accY.append(float(heart_message[i].split(',')[8]))
     accZ.append(float((heart_message[i].split(',')[9])))
     i += 1
accX = np.array(accY)

new_time = remove_first_x_elements(time, int((len(time)/10)))
new_time = new_time - new_time[0]
new_accx = remove_first_x_elements(accX, int((len(time)/10)))
accY = remove_first_x_elements(accY, int((len(time)/10)))
accZ = remove_first_x_elements(accZ, int((len(time)/10)))
time = remove_last_x_elements(new_time, int(len(new_time)/11))
accX = remove_last_x_elements(new_accx, int(len(new_time)/11))
accY = remove_last_x_elements(accY, int(len(new_time)/11))
accZ = remove_last_x_elements(accZ, int(len(new_time)/11))

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
low_frequency = 0.67
high_frequency = 1.67
nyquist_frequency = 0.5 * 40
low_cutoff = low_frequency / nyquist_frequency
high_cutoff = high_frequency / nyquist_frequency
order = 4

b, a = butter(order, [low_cutoff, high_cutoff], btype='band')
# Apply the filter to the acceleration data using filtfilt (forward and reverse filtering)
filtered_acc = filtfilt(b, a, detrended_accX)

#--------------------------------------------------------------------
#--------------------------------------------------------------------
#--------------------------------------------------------------------
# Take the absolute value of the filtered signal
abs_filtered_acc = np.maximum(filtered_acc, 0)

#threshold
threshold = 0.0025

# Find the peaks
peak_indices, _ = find_peaks(abs_filtered_acc, height = threshold)

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

# plt.xlim(0, 60)
# plt.plot(time, accX, label = 'Gyro X')
# plt.plot(time, accY, label = 'Gyro Y')
# plt.plot(time, accZ, label = 'Gyro Z')
# plt.xlabel('Time[sec]')
# plt.ylabel('Angular Velocity [rad/sec]')
# plt.title('Raw Gyro Data')
# plt.legend()

axes[0].plot(time, detrended_accX, label = "Subject 1 Raw Acceleration Data")
axes[0].set_xlim(0, 60)
axes[0].set_xlabel('Time[sec]')
axes[0].set_ylabel('Gyro [rad/sec]')
axes[0].set_title('Raw Heart Gyro Data')
axes[0].legend()

axes[1].plot(time, filtered_acc, label = 'Subject 1: 72BPM')
axes[1].set_xlim(0, 60)
axes[1].set_xlabel('Time[sec]')
axes[1].set_ylabel('Gyro [rad/sec]')
axes[1].set_title('IIR Bandpass Filtered Heartbeat')
axes[1].legend()

axes[2].plot(time, abs_filtered_acc, label = 'Subject 1: 72BPM')
axes[2].set_ylim(0, 0.025)
axes[2].set_xlim(0, 60)
axes[2].set_xlabel('Time[sec]')
axes[2].set_ylabel('Gyro [m/sec]')
axes[2].set_title('Extracted Peaks')
axes[2].legend()

# Add some space between the subplots
plt.subplots_adjust(hspace=0.8)

plt.show()