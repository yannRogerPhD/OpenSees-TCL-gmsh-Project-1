import numpy as np
import matplotlib.pyplot as plt

dt = 0.001  # time step (s)
tMax = 10.0  # total duration (s)
f0 = 2.0  # central frequency (Hz)
A = 0.1 * 9.81  # amplitude = 0.1 g in m/s^2

# ricker acceleration
t = np.arange(0, tMax, dt)
pi2 = (np.pi * f0 * (t - 1.0)) ** 2  # center at 1 s
acc = A * (1 - 2 * pi2) * np.exp(-pi2)

# integrate to velocity
vel = np.cumsum(acc) * dt  # numerical integration
vel = vel - np.mean(vel)  # baseline correction (remove drift)

# velocity file
np.savetxt("rickerInputVelocity.txt", vel, fmt="%.6e")
print("Saved rickerInputVelocity.txt with", len(vel), "points")


plt.figure(figsize=(10, 5))

plt.subplot(2, 1, 1)
plt.plot(t, acc, label="Acceleration")
plt.xlim(0, 4)
plt.ylabel("Accel [m/s²]")
plt.title("Ricker Acceleration Input")
plt.grid(True)

plt.subplot(2, 1, 2)
plt.plot(t, vel, color='orange', label="Velocity")
plt.xlim(0, 4)
plt.xlabel("Time [s]")
plt.ylabel("Velocity [m/s]")
plt.title("Integrated Velocity Input")
plt.grid(True)

plt.tight_layout()
plt.show()
