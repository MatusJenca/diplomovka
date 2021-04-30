import numpy as np
import matplotlib.pyplot as plt
from selfenergy_1d import selfEnergy,selfEnergyNoInt
from constants import *
from derivative import derivative
DELTA=1e-3
def densityOfStates(w,τ=100*τ0,seFunc=selfEnergy):
    #hranica integralu cez q
    qmx=1/(τ0*vf)
    qmx=qmx/ks
    #print(τ0)
    def diff(x):
        return -seFunc(x,τ=τ0,qmax=qmx)+seFunc(x,τ=τ,qmax=qmx)
    return derivative(diff,w,DELTA)
   
if __name__=="__main__": 
    Erg=np.linspace(0.2,1.8,100)
    ρ=np.array([densityOfStates(ε,seFunc=selfEnergyNoInt) for ε in Erg])
    #ρ2=np.array([densityOfStates(ε,τ=100*τ0,seFunc=selfEnergy) for ε in Erg])
    plt.plot(Erg,ρ,linewidth=1,label=r"hustota stavov τ0=$6.6\times10^{-16}$")
    #plt.plot(Erg,ρ2,linewidth=1,label=r"hustota stavov τ0=$3.310^{-15}$")
    plt.xlabel(r"$\frac{E}{E_{fermi}}$")
    plt.ylabel(r"ρ")
    plt.legend() 
    plt.show()
