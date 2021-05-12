import sys
sys.path.append('tools')
import numpy as np
import matplotlib.pyplot as plt
from selfenergy import SelfEnergy
from density import DOSDirect
if __name__=="__main__": 
    Erg=np.linspace(0.2,1.8,100)
    dosFunc=DOSDirect()
    ρ=np.array([dosFunc(ε) for ε in Erg])
    plt.plot(Erg,ρ,linewidth=1,label=r"hustota stavov τ0=$6.6\times10^{-16}$")
    plt.xlabel(r"$\frac{E}{E_{fermi}}$")
    plt.ylabel(r"ρ")
    plt.legend()
    plt.show()
