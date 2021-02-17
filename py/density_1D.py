import numpy as np
import matplotlib.pyplot as plt
from selfenergy_1d import selfEnergy,uf
DELTA=1e-3
ρ0=1
def densityOfStates(w):
    derivative=(selfEnergy(w+DELTA)-selfEnergy(w-DELTA))/(2*DELTA)
    return derivative
if __name__=='__main__':
    W=np.linspace(10,2*uf,100)
    ρ=np.array([densityOfStates(w) for w in W])
    plt.plot(W,ρ)
    plt.show()


