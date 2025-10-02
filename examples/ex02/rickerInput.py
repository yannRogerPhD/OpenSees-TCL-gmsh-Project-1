import numpy as np
import matplotlib.pyplot as plt

# parameters
dt = 0.001       # time step (s)
tMax = 10.0      # total duration (s)
f0 = 2.0         # central frequency (Hz)
A = 0.1 * 9.81   # amplitude = 0.1 g in m/s^2

# ricker wavelet
t = np.arange(0, tMax, dt)
pi2 = (np.pi * f0 * (t - 1.0))**2  # center at 1.0 s
ricker = A * (1 - 2*pi2) * np.exp(-pi2)

np.savetxt("ricker_input.txt", ricker, fmt="%.6e")
print("Saved ricker_input.txt with", len(ricker), "points")


plt.figure(figsize=(8, 4))
plt.plot(t, ricker, label="Ricker wavelet (f0=2 Hz, 0.1g)")
plt.xlim(0, 4)   # zoom into first 4 seconds
plt.xlabel("Time [s]")
plt.ylabel("Acceleration [m/s²]")
plt.title("Ricker Wavelet Input Motion")
plt.grid(True)
plt.legend()
plt.show()
