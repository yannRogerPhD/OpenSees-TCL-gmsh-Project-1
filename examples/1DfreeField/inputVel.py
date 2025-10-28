import numpy as np
import matplotlib.pyplot as plt

plt.style.use("MyLaTeXPlotStyle")

dt = 0.001
tMax = 10.0
t0 = 2.0
fc = 2.0

# tWindowPulse = (1 / fc) * 2

a = 1 / (np.sqrt(2) * np.pi * fc)
t = np.arange(0, tMax, dt)

var = ((t - t0) / a) ** 2
accel = (1 / np.sqrt(a)) * (1 - var) * np.exp(- 0.5 * var)
vel = - (1 / np.sqrt(a)) * (t - t0) * np.exp(- 0.5 * var)

# plt.plot(t, accel)
# plt.xlabel("time (s)")
# plt.ylabel("outcrop acceleration (m/s$^2$)")
plt.plot(t, vel)
plt.xlabel("time (s)")
plt.ylabel("outcrop velocity (m/s)")
plt.show()

np.savetxt("velInput.out", vel, fmt="%.6e")
