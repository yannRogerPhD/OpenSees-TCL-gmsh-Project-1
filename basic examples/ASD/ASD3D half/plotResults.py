import numpy as np
import matplotlib.pyplot as plt

plt.style.use("MyLaTeXPlotStyle")

time = np.loadtxt("soilBase.txt")[:, 0]
accelBase = np.loadtxt("soilBase.txt")[:, 1]
accelTop = np.loadtxt("soilTopZ.txt")[:, 1]
accelTopY = np.loadtxt("soilTopY.txt")[:, 1]

plt.plot(time, accelTop, color="black", label="TopZ")
# plt.plot(time, accelTopY, color="black", label="TopY")
plt.plot(time, accelBase, color="orange", label="BotZ")
plt.title("validation of 3D ASD absorbing boundaries")
plt.xlabel("time (s)")
plt.ylabel("accel X (in g)")
plt.legend()
plt.show()
