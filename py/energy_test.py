from tools.selfenergy import SelfEnergy
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    se = SelfEnergy(qmax=10)
    erg = np.linspace(0.01, 1.5, 100)
    self_erg = np.array([se(e, taucoef=1) for e in erg])
    test = np.array([se.test(e) for e in erg])
    plt.plot(erg, self_erg)
    #plt.plot(erg, test)
    plt.show()
