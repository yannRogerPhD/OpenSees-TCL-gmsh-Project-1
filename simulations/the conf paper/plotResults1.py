import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("results1/accelRigidBaseSPConf.out")
t = data[:, 0]

# nodes = {6: 1, 19: 4, 23: 7, 27: 10}
nodes = {6: 1, 27: 10}

# X acceleration
for nid, col in nodes.items():
    plt.figure()
    plt.plot(t, data[:, col], linewidth=1.5)
    plt.xlabel("Time (s)")
    plt.ylabel("aX (m/s²)")
    plt.title(f"Node {nid} — X acceleration")
    plt.grid(True, alpha=0.3)

# Z acceleration
for nid, col in nodes.items():
    plt.figure()
    plt.plot(t, data[:, col + 2], linewidth=1.5)
    plt.xlabel("Time (s)")
    plt.ylabel("aZ (m/s²)")
    plt.title(f"Node {nid} — Z acceleration")
    plt.grid(True, alpha=0.3)

# # Fourier spectrum (X)
# dt = t[1] - t[0]
# for nid, col in nodes.items():
#     signal = data[:, col]
#     freqs = np.fft.rfftfreq(len(signal), d=dt)
#     amps = np.abs(np.fft.rfft(signal)) * 2.0 / len(signal)
#     plt.figure()
#     plt.plot(freqs, amps, linewidth=1.5)
#     plt.xlabel("Frequency (Hz)")
#     plt.ylabel("|FFT|")
#     plt.title(f"Node {nid} — Fourier spectrum (X)")
#     plt.xlim(0, 20)
#     plt.grid(True, alpha=0.3)

plt.show()
