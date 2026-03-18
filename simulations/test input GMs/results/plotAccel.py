"""
Plot acceleration time histories from OpenSees output.
"""
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('MyLaTeXPlotStyle')

# load data: columns are [time, accelX, accelY, accelZ]
data = np.loadtxt("accelerationRef.out")
data2 = np.loadtxt("acceleration.out")
data3 = np.loadtxt("accelRigidBase.out")

t = data[:, 0]
ax = data[:, 1]
ax2 = data2[:, 1]
ax3 = data3[:, 1]

ay = data[:, 2]
az = data[:, 3]

ax = ax/9.81
ay = ay/9.81
az = az/9.81

ax2 = ax2/9.81
ax3 = ax3/9.81

plt.plot(t, ax3, label="accelRigidBase")
plt.plot(t, ax2, label="accelFreeField")
plt.plot(t, ax, label="accelRef")

plt.legend()
plt.legend()
plt.show()

