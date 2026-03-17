import matplotlib.pyplot as plt
import numpy as np

plt.style.use("MyLaTeXPlotStyle")

acc = np.loadtxt("elcentro.txt")
g = 9.81
# print(len(acc))
n = len(acc)

dt = 0.005
time = np.arange(n) * dt

plt.plot(time, acc/g, color="blue", linewidth=2.0)
plt.ylabel("acceleration in $[g]$")
plt.show()

matLoose = {i: 1 for i in range(1, 6)}
matDense = {j: 2 for j in range(6, 11)}
customMaterialMap = matLoose | matDense
# print(customMaterialMap)
