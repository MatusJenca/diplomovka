import sys

sys.path.append('./tools')
import numpy as np
import matplotlib.pyplot as plt
from integrator import Newton, EPSILON
from selfenergy import SelfEnergy
seFunc = SelfEnergy()
if __name__ == '__main__':
    erg = np.linspace(0.8, 1.2, 100)
    se = np.array([seFunc(e, taucoef=1) for e in erg])
    se100 = np.array([seFunc(e, taucoef=100) for e in erg])
    diff = se - se100
    plt.plot(erg, se)
    plt.plot(erg, se100)
    plt.plot(erg, diff)
    plt.show()
