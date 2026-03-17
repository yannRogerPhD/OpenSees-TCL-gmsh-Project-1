import matplotlib.pyplot as plt
import numpy as np

plt.style.use("MyLaTeXPlotStyle")

time = np.loadtxt("soilBase.txt")[:, 0]
accelTop = np.loadtxt("soilTopP.txt")[:, 1]
accelBot = np.loadtxt("soilBase.txt")[:, 1]

plt.plot(time, accelTop)
plt.plot(time, accelBot)

plt.show()
