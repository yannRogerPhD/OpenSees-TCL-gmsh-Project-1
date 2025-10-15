import numpy as np
import matplotlib.pyplot as plt

# Parameters
fc = 5.0        # Central frequency (Hz)
dt = 0.0025      # Time step (s)
npts = 4000     # Number of points
t0 = (1.0 / fc) * 0.25  # Delay to center the wavelet

# Time array
t = np.arange(0, npts * dt, dt)

# Ricker wavelet (velocity form)
A = 1.0
pi2fc2 = (np.pi**2) * (fc**2)
ricker = A * (1.0 - 2 * pi2fc2 * (t - t0)**2) * np.exp(-pi2fc2 * (t - t0)**2)

plt.plot(t, ricker)
plt.show()

f = np.fft.rfftfreq(len(t), dt)
rickerFB = np.fft.rfft(ricker)

rickerF = np.abs(rickerFB)

plt.plot(f, rickerF)
plt.show()

# Save to file
np.savetxt("rickerVelocity.txt", ricker, fmt="%.8e")
