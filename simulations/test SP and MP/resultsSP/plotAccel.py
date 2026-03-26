"""
Plot acceleration time histories from OpenSees output.
"""
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('MyLaTeXPlotStyle')

# load data: columns are [time, accelX, accelY, accelZ]
data = np.loadtxt("accelerationRef.out")
# data2 = np.loadtxt("acceleration.out")
data1 = np.loadtxt("accelRigidBase1.out")
data2 = np.loadtxt("accelRigidBase2.out")
data3 = np.loadtxt("accelRigidBaseSP4.out")

t = data[:, 0]
ax = data[:, 1]
# ax2 = data2[:, 1]
ax1 = data1[:, 1]
ax2 = data2[:, 1]
ax3 = data3[:, 1]

ay = data[:, 2]
az = data[:, 3]

ax = ax/9.81
ay = ay/9.81
az = az/9.81

# ax2 = ax2/9.81
ax1 = ax1/9.81
ax2 = ax2/9.81
ax3 = ax3/9.81

plt.plot(t, ax1, label="accelRBZ2Y10X10")
plt.plot(t, ax2, label="accelRBZ1Y10X10")
plt.plot(t, ax3, label="accelRBZ4Y10X10")
# plt.plot(t, ax2, label="accelFreeField")
plt.plot(t, ax, label="accelRef", linewidth=1.5)

plt.legend()
plt.legend()
plt.show()

