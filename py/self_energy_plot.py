import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('tools')
from selfenergy import SelfEnergy

seFunc = SelfEnergy(qmax=10)
if __name__ == '__main__':
    erg = np.linspace(0.01, 1.5, 100)
    se = np.array([seFunc(e) for e in erg])
    plt.xlabel(r"$\frac{ε}{E_{Fermi}}$[ 1 ]")
    plt.ylabel(r"$Σ_{self}$ [ J ]")
    plt.plot(erg, se)
    plt.savefig("../img/self_energy_plot.pdf")


