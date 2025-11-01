import numpy as np
import matplotlib.pyplot as plt

plt.style.use("MyLaTeXPlotStyle")

accelTopV = np.loadtxt("velTop.out")
accelBotV2 = np.loadtxt("velBot.out")
accelBotV = np.loadtxt("velInput.out")

accelTop = accelTopV[:, 1]
# accelBot = accelBotV[:, 1]
accelBot = accelBotV[:]
accelBot2 = accelBotV2[:, 1]

time = accelTopV[:, 0]
dt = 0.001
nVals = len(time)

fVals = np.fft.rfftfreq(nVals, dt)
topFFT = np.fft.rfft(accelTop)
botFFT = np.fft.rfft(accelBot)
botFFT2 = np.fft.rfft(accelBot2)

numTF = np.abs(topFFT) / np.abs(botFFT)
numTF2 = np.abs(topFFT) / np.abs(botFFT2)

# plt.plot(fVals, numTF)
# # plt.plot(fVals, numTF2)
# plt.xlim(0.1, 7)
# plt.ylim(0.0, 6.0)
# plt.show()


h = 30.0
cs = 230.9
rho = 1755
cb = 1010.0
rho_b = 2000.0
alpha = (rho * cs) / (rho_b * cb)

# analytical transfer function
omega = 2 * np.pi * fVals
arg = omega * h / cs
T_noDamp = 1.0 / np.sqrt(np.cos(arg) ** 2 + (alpha ** 2) * np.sin(arg) ** 2)

# plt.plot(fVals, T_noDamp, label="analytical (no damping)", ls="--", lw=2, alpha=0.7)
# plt.plot(fVals, numTF, label="Numerical", lw=2, alpha=0.7)
plt.plot(fVals, T_noDamp, label="analytical (no damping)", ls="--", lw=3, alpha=0.75, color='black')
plt.plot(fVals, numTF, label='OpenSees (no damping)', lw=2, alpha=0.9, color='orange')
plt.xlim(0.101, 7.0)
plt.ylim(0, 5.1)
plt.legend(fontsize=10, loc='upper center', bbox_to_anchor=(0.555, 1.0))
plt.xlabel("time (s)", fontsize=15)
plt.ylabel("outcrop velocity (m/s)", fontsize=15)
plt.tick_params(axis='both', which='major', labelsize=15)
ax = plt.gca()
for spine in ax.spines.values():
    spine.set_linewidth(0.85)  # Default is usually 1.0-1.5
plt.grid(False)
# plt.savefig("plot_name.pdf", bbox_inches='tight')
plt.show()
