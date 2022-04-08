import sys
sys.path.append('tools')
import numpy as np
import matplotlib.pyplot as plt
from selfenergy import SelfEnergy
from density import DensityOfStates
if __name__=="__main__": 
    Erg=np.linspace(0.8,1.2,100)
    seFunc=SelfEnergy()
    seFunc5=SelfEnergy(τ0=5*6.58e-16)
    dosFunc=DensityOfStates(seFunc)
    dosFunc5=DensityOfStates(seFunc5)
    ρ=np.array([dosFunc(ε) for ε in Erg])
    ρ5=np.array([dosFunc5(ε) for ε in Erg])

    plt.plot(Erg,ρ,linewidth=1,label=r"hustota stavov τ0=$6.6\times10^{-15}$")
    #plt.plot(Erg,ρ5,linewidth=1,label=r"hustota stavov τ0=$5*6.6\times10^{-15}$")
    plt.xlabel(r"$\frac{E}{E_{fermi}}$")
    plt.ylabel(r"ρ")
    plt.legend() 
    plt.show()
    '''
    plt.savefig('density_both.png')
    plt.clf()
    plt.plot(Erg,ρ,linewidth=1,label=r"hustota stavov τ0=$6.6\times10^{-16}$")
    plt.savefig('density_tau0.png')
    plt.clf()
    plt.plot(Erg,ρ5,linewidth=1,label=r"hustota stavov τ0=$5*6.6\times10^{-16}$")
    plt.savefig('density_5tau0')
    '''
