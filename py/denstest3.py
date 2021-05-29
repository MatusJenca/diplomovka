import sys
sys.path.append('tools')
import numpy as np
import matplotlib.pyplot as plt
from selfenergy import SelfEnergy
from density import DOSDirect,DOSDirectNoInt
if __name__=="__main__": 
    Erg=np.linspace(0.2,1.8,100)
    dosFunc=DOSDirectNoInt()
    dosFunc2=DOSDirect()
    ρ=np.array([dosFunc(ε) for ε in Erg])
    #ρ2=np.array([dosFunc2(ε) for ε in Erg])
    plt.plot(Erg,ρ,linewidth=1,label=r"hustota stavov bez integrovania")
    #plt.plot(Erg,ρ2,linewidth=1,label=r"hustota stavov s integrovanim")
    plt.xlabel(r"$\frac{E}{E_{fermi}}$")
    plt.ylabel(r"ρ")
    plt.legend()
    plt.show()
