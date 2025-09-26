import numpy as np
import matplotlib.pyplot as plt

dt = 0.001
h = 30.0
cs = 230.9
rho = 1755
cb = 1010.0
rho_b = 2000.0
alpha = (rho * cs) / (rho_b * cb)
zeta = 0.008  # 0.8% damping


surf = np.loadtxt('surfAcc.out')  # time, accel
base = np.loadtxt("baseAcc.out")


# first column = times, second = acceleration
t = surf[:, 0]
surf_acc = surf[:, 1]
base_acc = base[:, 1]

# compute FFTs
n = len(t)
freq = np.fft.rfftfreq(n, dt)
SurfFFT = np.fft.rfft(surf_acc)
BaseFFT = np.fft.rfft(base_acc)

# avoid divide-by-zero
eps = 1e-15
TF_num = np.abs(SurfFFT) / (np.abs(BaseFFT) + eps)

# analytical transfer function
omega = 2 * np.pi * freq
arg = omega * h / cs
T_noDamp = 1.0 / np.sqrt(np.cos(arg) ** 2 + (alpha ** 2) * np.sin(arg) ** 2)

# With damping
cs_star = cs * (1 + 1j * zeta)
arg_damp = omega * h / cs_star
T_damp = 1.0 / np.sqrt(np.cos(arg_damp) ** 2 + (alpha ** 2) * np.sin(arg_damp) ** 2)
T_damp = np.abs(T_damp)


plt.figure(figsize=(9, 6))
plt.plot(freq, TF_num, label="Numerical (OpenSees)", lw=2)
plt.plot(freq, T_noDamp, label="Analytical (ζ=0%)", ls="--", lw=2)
plt.plot(freq, T_damp, label="Analytical (ζ=0.8%)", ls=":", lw=2)

plt.xlim(0, 7)
plt.ylim(0, 55)
plt.xlabel("Frequency [Hz]")
plt.ylabel("|T(f)|")
plt.title("Transfer Function Comparison (Surface/Base)")
plt.grid(True)
plt.legend()
plt.show()
