import numpy as np
import matplotlib.pyplot as plt

plt.style.use("MyLaTeXPlotStyle")

plt.style.use('~/Desktop/phd/OpenSees/SSI/OpenSeesPy/plotLaTeX/MyPyTexPlot.mplstyle')

aValues = np.loadtxt('accelTopResults.out')

tVals = aValues[:, 0]
axVals = aValues[:, 1]

g = 9.81

axValsN = axVals / g

plt.plot(tVals, axValsN)
plt.xlim(0, None)
plt.show()
