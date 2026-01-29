import numpy as np
import matplotlib.pyplot as plt

plt.style.use("MyLaTeXPlotStyle")

time = np.loadtxt("topNode588_accel_XYZ.out")[:, 0]
accelX = np.loadtxt("topNode588_accel_XYZ.out")[:, 1]

plt.plot(time, accelX / (5 * (9.81 ** 2)), color="black", label="TopZ")
# plt.plot(time, accelTopY, color="black", label="TopY")
# plt.plot(time, accelBase, color="orange", label="BotZ")
# plt.title("validation of 3D ASD absorbing boundaries")
plt.xlabel("time (s)")
plt.ylabel("accel X (in g)")
plt.legend()
plt.show()
