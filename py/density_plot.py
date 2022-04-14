import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append('tools')
from density import DensityOfStates
from selfenergy import SelfEnergy

sefunc = SelfEnergy()
dfunc = DensityOfStates(sefunc)
if __name__ == "__main__":
    erg = np.linspace(0.8, 1.2, 100)
    dens = np.array([dfunc(e) for e in erg])
    plt.xlabel(r"$\frac{ε}{E_{Fermi}}$[ 1 ]")
    plt.ylabel(r"$\rho_{self}[m^{-3}]$")
    plt.plot(erg, dens)
    plt.savefig("../img/density_plot.pdf")
