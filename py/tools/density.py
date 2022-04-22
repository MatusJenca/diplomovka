import numpy as np
from selfenergy import SelfEnergy
from tools.derivative import derivative
from tools.integrator import Newton, EPSILON


class DensityOfStates:
    def __init__(self, seFunc):
        assert issubclass(type(seFunc), SelfEnergy)
        self.seFunc = seFunc
        self.DELTA = 1e-3

    def __call__(self, erg, taucoef=100):
        def diff(x):
            return self.seFunc(x, taucoef=100) - self.seFunc(x, taucoef=1)

        # return diff(erg)/self.seFunc.Ef
        res = derivative(diff, erg, self.DELTA) / self.seFunc.Ef
        # print(res)
        return res


