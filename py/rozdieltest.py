import sys
sys.path.append('./tools')
import numpy as np
import matplotlib.pyplot as plt
from integrator import Newton,EPSILON
from selfenergy import SelfEnergy
from math import pi as π

seFunc=SelfEnergy()
if __name__=='__main__':

    Erg=np.linspace(0.7,1.3,100)
    Σ=np.array([seFunc(ε) for ε in Erg])/seFunc.Ef
    Σ100=np.array([seFunc(ε,taucoef=100) for ε in Erg])/seFunc.Ef
    rozdiel=Σ-Σ100
    plt.xlabel(r"$\frac{ε}{E_{Fermi}}$[ 1 ]")
    plt.ylabel(r"$Σ_{self}$ [ J ]")
    plt.plot(Erg,Σ,linewidth=1,label="τ=τ0")
    plt.plot(Erg,Σ100,linewidth=1,label="τ=$\infty$")
    plt.plot(Erg,rozdiel,linewidth=1,label="rozdiel")
    plt.legend() 
    plt.show()
