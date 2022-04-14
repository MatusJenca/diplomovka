import numpy as np
import matplotlib.pyplot as plt
import sys

sys.path.append('tools')
from density import DensityOfStates
from selfenergy import SelfEnergy

sefunc = SelfEnergy()
sefunc10 = SelfEnergy(τ0=10*6.58e-15)
sefunc01 = SelfEnergy(τ0=0.1*6.58e-15)
sefunc001 = SelfEnergy(τ0=0.01*6.58e-15)
dfunc = DensityOfStates(sefunc)
dfunc10 = DensityOfStates(sefunc10)
dfunc01 = DensityOfStates(sefunc01)
dfunc001 = DensityOfStates(sefunc001)

if __name__ == "__main__":
    erg = np.linspace(0.8, 1.2, 100)
    dens = np.array([dfunc(e) for e in erg])
    #dens10 = np.array([dfunc10(e) for e in erg])
    #dens01 = np.array([dfunc01(e) for e in erg])
    #dens001 = np.array([dfunc001(e) for e in erg])
    plt.xlabel(r"$\frac{ε}{E_{Fermi}}$[ 1 ]")
    plt.ylabel(r"$\rho_{self}[m^{-3}]$")
    plt.plot(erg, dens, label=r"$\tau=\tau_0$")
    #plt.plot(erg, dens10, label=r"$\tau=10\ \tau_0$")
    #plt.plot(erg, dens01, label=r"$\tau=0.1\ \tau_0$")
    #plt.plot(erg, dens001, label=r"$\tau=0.01\ \tau_0$")
    plt.legend()
    plt.show()