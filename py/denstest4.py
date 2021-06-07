import sys
sys.path.append('tools')
import numpy as np
import matplotlib.pyplot as plt
from selfenergy import SelfEnergy
from density import DOSDirect,DensityOfStates
if __name__=="__main__": 
    Erg=np.linspace(0.2,1.8,100)
    dosFunc=DOSDirect()
    seFunc=SelfEnergy()
    dosFunc2=DensityOfStates(seFunc)
    ρ=np.array([dosFunc(ε) for ε in Erg])
    ρ2=np.array([dosFunc2(ε) for ε in Erg])
    print("ρ:",ρ)
    print("ρ2:",ρ2)
    print("pomer:",ρ/ρ2)
    plt.plot(Erg,ρ,linewidth=1,label=r"hustota stavov analyticka derivacia")
    #plt.plot(Erg,ρ2,linewidth=1,label=r"hustota stavov numericka derivacia")
    plt.xlabel(r"$\frac{E}{E_{fermi}}$")
    plt.ylabel(r"ρ")
    plt.legend()
    plt.show()
