import numpy as np
import matplotlib.pyplot as plt

velValuesI = np.loadtxt('velHistory.out')
velResultsTop = np.loadtxt('velTopResults.out')
velResultsBottom = np.loadtxt('velBotResults.out')

velTopO = velResultsTop[:, 1]
velBotO = velResultsBottom[:, 1]

timeVals = velResultsTop[:, 0]

dt = 0.005

nVals = len(timeVals)

freqValues = np.fft.rfftfreq(nVals, dt)
omegaVals = 2 * np.pi * freqValues

h = 40.0
VsS = 250
rhoSoil = 1.7
VsB = 760
rhoB = 2.4

alphaSquared = (rhoSoil * VsS) / (rhoB * VsB)
theta = omegaVals * h / VsS

TFmod = 1 / np.sqrt((np.cos(theta)) ** 2 + (alphaSquared * np.cos(theta)) ** 2)

plt.plot(freqValues, TFmod)
plt.xlim(0, 6)
plt.ylim(0, 150)
plt.show()
