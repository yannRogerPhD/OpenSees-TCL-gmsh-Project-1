import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft

plt.style.use("MyLaTeXPlotStyle")

fileName = "accelTop.out"

nDOF = 2

dampT = 0.05

# choose nPeriodT values between 100 - 500
nPeriodT = 400

# kT has no effect on the shape or ampl of the response spectra, only on internal num conditioning of the TF computation
kT = 1000


def respSpectra(a, T, nStep, nPeriod=nPeriodT, damp=dampT, k=kT):
    a = np.concatenate(([0], a)) * 9.81
    minPower = -3
    maxPower = 1
    p = np.logspace(minPower, maxPower, nPeriod)
    dw = 2 * np.pi / T
    # w = np.arange(0, (nStep + 1) * dw, dw)
    w = np.linspace(0, nStep * dw, nStep + 1)
    aFFT = fft(a)
    uMax = np.zeros(nPeriod)
    vMax = np.zeros(nPeriod)
    aMax = np.zeros(nPeriod)

    for j in range(nPeriod):
        m = ((p[j] / (2 * np.pi)) ** 2) * k
        c = 2 * damp * (k * m) ** 0.5
        H = 1 / (-m * w[:(nStep // 2) + 1] ** 2 + 1j * c * w[:(nStep // 2) + 1] + k)
        H = np.concatenate((H, np.conj(H[1:nStep // 2 + 1][::-1])))

        qFFT = -m * aFFT
        u = H * qFFT
        utime = np.real(ifft(u))
        uMax[j] = np.max(np.abs(utime))
        vMax[j] = (2 * np.pi / p[j]) * uMax[j]
        aMax[j] = (2 * np.pi / p[j]) * vMax[j] / 9.81

    return p, uMax, vMax, aMax


def accelPlot():
    """
    acceleration files in OpenSees have the form below:
        time || node1DOF1 | node1DOF2 || node2DOF1 | node2DOF2 || ... || nodeNDOFn | nodeNDOFn
    """
    acc = np.loadtxt(fileName)
    time = acc[:, 0]
    acc = np.delete(acc, 0, axis=1)
    nStep, nAcc = acc.shape
    '''
    THE ASSERT CONDITION IN PYTHON
        - It is given as:
            <assert condition, "optional message if condition fails">
            - if the condition is true, nothing happens
            - if the condition is false, the program stops and prints the message
        - see example below in our case
    '''
    assert nAcc % nDOF == 0, "Column count not compatible with DOF = 2"
    nNode = nAcc // nDOF
    """
    1. the current order is:
        - [node1DOF1, node1DOF2, node2DOF1, node2DOF2, ..., nodeNDOFn, nodeNDOFn]
        - assuming n nodes
    2. now we want to be able to index acceleration values as this: 
        - a[timeIndex, DOFIndex, nodeIndex]
    """
    a = acc.reshape(nStep, nNode, nDOF) / 9.81

    plt.figure(1)
    plt.plot(time, a[:, nNode - 1, 0], '-b', linewidth=2.5)
    # plt.plot(time, a[:, nNode - 1, 0], '-b')
    plt.grid(True)
    plt.xlabel('time (sec)', fontsize=20)
    plt.ylabel('acceleration (g)', fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.tight_layout()
    # plt.savefig("surfaceAccel.pdf", bbox_inches='tight')
    plt.show()

    p, uMax, vMax, aMax = respSpectra(a[:, nNode - 1, 0].copy(), time[-1], nStep)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6, 6))

    ax1.semilogx(p, aMax, 'orange', linewidth=2.5)
    ax1.grid(True, which="minor", linestyle="--", linewidth=1.5)  # log-type grid
    # ax1.grid(True, which="both", linestyle="--", linewidth=0.5)  # log-type grid
    ax1.set_ylabel('$\\text{S}_a (g)$', fontsize=20)
    ax1.set_xticklabels([])
    ax1.tick_params(axis='both', which='major', labelsize=16)

    ax2.semilogx(p, vMax, 'orange', linewidth=2.5)
    ax2.grid(True, which="minor", linestyle="--", linewidth=1.5)  # log-type grid
    ax2.set_ylabel('$\\text{S}_v$ (m/s)', fontsize=20)
    ax2.set_xticklabels([])
    ax2.tick_params(axis='both', which='major', labelsize=16)

    ax3.semilogx(p, uMax, 'orange', linewidth=2.5)
    ax3.grid(True, which="minor", linestyle="--", linewidth=1.5)  # log-type grid
    ax3.set_ylabel('$\\text{S}_d$ (m)', fontsize=20)
    ax3.set_xlabel('Period, T (sec)', fontsize=20)
    # ax3.set_xticklabels([])
    ax3.tick_params(axis='both', which='major', labelsize=16)

    # plt.savefig('logSpectra.png')
    # plt.xlabel('Period, T (sec)', fontsize=25)
    # plt.tick_params(axis='both', which='major', labelsize=16)
    plt.subplots_adjust(hspace=0.15)  # control vertical spacing (default is ~0.2-0.3)
    # plt.savefig("logSpectra.pdf", bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    accelPlot()
