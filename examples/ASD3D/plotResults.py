import numpy as np
import matplotlib.pyplot as plt

plt.style.use("MyLaTeXPlotStyle")

time = np.loadtxt("soilBase.txt")[:, 0]
accelBase = np.loadtxt("soilBase.txt")[:, 1]
accelTop = np.loadtxt("soilBott.txt")[:, 1]

plt.plot(time, accelTop)
plt.plot(time, accelBase)
plt.show()
