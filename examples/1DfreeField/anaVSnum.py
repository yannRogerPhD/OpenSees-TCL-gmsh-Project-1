import numpy as np
import matplotlib.pyplot as plt

accelTopV = np.loadtxt("accelTop.out")
accelBotV = np.loadtxt("accelBot.out")

accelTop = accelTopV[:, 1]
accelBot = accelBotV[:, 1]

time = accelBotV[:, 0]
dt = 0.001
nVals = len(time)

fVals = np.fft.rfftfreq(nVals, dt)
topFFT = np.fft.rfft(accelTop)
botFFT = np.fft.rfft(accelBot)

numTF = np.abs(topFFT) / np.abs(botFFT)

plt.plot(fVals, numTF)
plt.show()