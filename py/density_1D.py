import numpy as np
import matplotlib.pyplot as plt
from selfenergy_1d import selfEnergy
from constants import *
from derivative import derivative
DELTA=1e-3
def densityOfStates(w):
    #hranica integralu cez q
    qmx=1/(τ0*vf)
    qmx=qmx/ks
    def diff(x):
        return -selfEnergy(x,qmax=qmx)+selfEnergy(x,τ=100*τ0,qmax=qmx)
    return derivative(diff,w,DELTA)
   
if __name__=="__main__": 
    Erg=np.linspace(0.2,1.8,100)
    ρ=np.array([densityOfStates(ε) for ε in Erg])
    plt.plot(Erg,ρ,linewidth=1,label="hustota stavov")
    plt.legend() 
    plt.show()
