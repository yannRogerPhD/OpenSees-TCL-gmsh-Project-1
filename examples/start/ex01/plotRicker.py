import numpy as np
import matplotlib.pyplot as plt

# plt.style.use("MyLaTeXPlotStyle")

# print(plt.style.available)

with open('rickerInputVelocity.txt') as f:
    lines = f.readlines()

velValues = np.loadtxt("rickerInputVelocity.txt")
accelValues = np.loadtxt("accelTop.out")

accelTop = accelValues[:, 1]

dt = 0.001

velResBot = np.loadtxt('velBot.out')
vResBot = velResBot[:, 1]
timeVals = velResBot[:, 0]

velResTop = np.loadtxt('velTop.out')
vResTop = velResTop[:, 1]

# plt.plot(timeVals, vResBot, color='green', linewidth=4)
# plt.plot(timeVals, vResTop, color='blue', linewidth=3)
# plt.show()

nVals = len(timeVals)

vInput = np.loadtxt('rickerInputVelocity.txt')
vInput = vInput[:nVals]

fVals = np.fft.rfftfreq(nVals, dt)
topFFT = np.fft.rfft(vResTop)
botFFT = np.fft.rfft(vInput)

numTF = np.abs(topFFT) / np.abs(botFFT)

h = 30.0
VsSoil = 230.9
VsRock = 1010.0
rhoSoil = 1755
rhoRock = 2000
alpha = (rhoSoil * VsSoil) / (rhoRock * VsRock)
om = 2 * np.pi * fVals
theta = om * h / VsSoil

noDampingT = 1.0 / np.sqrt((np.cos(theta)) ** 2 + (alpha * np.sin(theta)) ** 2)

plt.plot(fVals, numTF, color='blue', label="OpenSees", ls='--')
plt.plot(fVals, noDampingT, color='orange', label="analytical", ls=':')
plt.xlim(0.20, 7.5)
plt.ylim(0, 5.5)
plt.legend()
plt.show()

plt.plot(timeVals, accelTop, color="black")
plt.show()
