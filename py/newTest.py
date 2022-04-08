import sys
sys.path.append('./tools')
import numpy as np
import matplotlib.pyplot as plt
from integrator import Newton,EPSILON
from selfenergy import SelfEnergy
from math import pi as π

seFunc=SelfEnergy(qmax=10)
if __name__=='__main__':

    Erg=np.linspace(0.01,1.5,100)
    Σ=np.array([seFunc(ε) for ε in Erg])
    Σ100=np.array([seFunc(ε,taucoef=100) for ε in Erg])
    test=np.array([seFunc.test(eps) for eps in Erg])
    plt.xlabel(r"$\frac{ε}{E_{Fermi}}$[ 1 ]")
    plt.ylabel(r"$Σ_{self}$ [ J ]")
    plt.xlim(0,1.5)
    print(Σ100/test)
    plt.plot(Erg,Σ,linewidth=1,label="τ=τ0")
    plt.plot(Erg,Σ100,linewidth=1,label="τ=$\infty$")
    plt.plot(Erg,test,linewidth=1,label="test")
    plt.legend() 
    #plt.show()
    plt.savefig('../img/self_energy_comp')
