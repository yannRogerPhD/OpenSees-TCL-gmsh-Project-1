"""
Plot pore pressure time history from OpenSees output.
"""
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('MyLaTeXPlotStyle')

# load data: columns are [time, porePressure]
data1 = np.loadtxt("porePressureRB.out")
data2 = np.loadtxt("porePressureRef.out")

t1 = data1[:, 0]
pp1 = data1[:, 1]

t2 = data2[:, 0]
pp2 = data2[:, 1]

plt.plot(t1, pp1, label="rigid based")
# plt.plot(t2, pp2, label="reference dashpot")
plt.xlabel("Time (s)")
plt.ylabel("Pore Pressure (kPa)")
plt.title("Pore Pressure Time History")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
