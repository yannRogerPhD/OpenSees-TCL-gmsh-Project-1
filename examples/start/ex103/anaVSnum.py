import numpy as np
import matplotlib.pyplot as plt

plt.style.use("MyLaTeXPlotStyle")

# velValuesIO = np.loadtxt('velHistory.out')
velValuesI = np.loadtxt('rickerVelocity.txt')
velResultsTop = np.loadtxt('velTopResultsEll.out')
velResultsBottom = np.loadtxt('velBotResultsEll.out')

velTopO = velResultsTop[:, 1]
velBotO = velResultsBottom[:, 1]

timeVals = velResultsTop[:, 0]

dt = 0.0025

nVals = len(timeVals)
velValuesI = velValuesI[:nVals]

freqValues = np.fft.rfftfreq(nVals, dt)
omegaVals = 2 * np.pi * freqValues

velTopFFT_O = np.fft.rfft(velTopO)
velBotFFT_O = np.fft.rfft(velBotO)
velValuesFFT_O = np.fft.rfft(velValuesI)

TF_num = np.abs(velTopFFT_O) / np.abs(velBotFFT_O)
TF_num2 = np.abs(velTopFFT_O) / np.abs(velValuesFFT_O)

h = 40.0
VsS = 250
rhoSoil = 1.7
VsB = 760
rhoB = 2.4

alphaSquared = (rhoSoil * VsS) / (rhoB * VsB)
theta = omegaVals * h / VsS

TF_ana = 1 / np.sqrt((np.cos(theta)) ** 2 + (alphaSquared * np.cos(theta)) ** 2)

plt.plot(freqValues, TF_ana, ls=':', color='black', label="analytical", lw=3.5, alpha=0.60, zorder=5)
plt.plot(freqValues, TF_num, ls='--', color='orange', label="OpenSees", lw=3.0, markevery=20, zorder=1)
# plt.plot(freqValues, TF_num2, ls='--', color='blue', label="OpsIncident", lw=3.0, markevery=20, zorder=1)
plt.xlim(0.2, 7.25)
plt.ylim(0, 80)
plt.legend()
plt.show()

# plt.plot(freqValues, np.abs(velValuesFFT_O), label='amplitude', color='orange')
# plt.plot(freqValues, np.unwrap(np.angle(velValuesFFT_O)), label='phase')
# plt.xlim(0.2, 10.25)
# plt.xlim(0, None)
# plt.show()


# # plt.plot(freqValues, np.abs(velValuesFFT_O), label='amplitude')
# plt.plot(freqValues, np.unwrap(np.angle(velValuesFFT_O)), label='phase')
# plt.xlim(0.2, 20.25)
# # plt.xlim(0, None)
# plt.show()

testNow = np.loadtxt('rickerVelocity.txt')

plt.plot(timeVals, testNow)
# plt.show()
dt = 0.005

fVals = np.fft.rfftfreq(len(timeVals), dt)
ampB = np.fft.rfft(testNow)

ampA = np.abs(ampB)

plt.plot(fVals, ampA)
# plt.show()
