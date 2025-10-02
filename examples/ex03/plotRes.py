import matplotlib.pyplot as plt
import numpy as np

plt.style.use('/home/yafeu/Desktop/Temporaire and Permanent/Temporaire/temp2/MyPyTexPlot.mplstyle')

# load the data
soil_base = np.loadtxt('soil_base.txt')
soil_top = np.loadtxt('soil_top.txt')

# extract time and acceleration
time_base = soil_base[:, 0]
acc_base = soil_base[:, 1]

time_top = soil_top[:, 0]
acc_top = soil_top[:, 1]

# plotting
plt.figure(figsize=(10, 6))
plt.plot(time_base, acc_base, label='Base Acceleration')
plt.plot(time_top, acc_top, label='Top Acceleration')

plt.xlabel('Time (s)')
plt.ylabel('Acceleration')
plt.title('Acceleration Time Histories: Base vs Top')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
