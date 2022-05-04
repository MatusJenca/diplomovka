import numpy as np
from tools.derivative import derivative
from tools.physfunction import PhysFunction
from math import pi


class DensityOfStates(PhysFunction):
    def __init__(self, seFunc):
        PhysFunction.__init__(self)
        self.seFunc = seFunc
        self.DELTA = 1e-3
        print("tau0:", self.seFunc.tau0)
        self.KONST1 = (self.vf * self.seFunc.tau0 * self.kf) ** 2
        self.KONST = 0.5 * ((3 * pi ** 3) * self.h * (self.vf ** 3) * (self.seFunc.tau0 ** 2) * self.rhof)
        print('Konst:', self.KONST)
        print('Konst1:', self.KONST1)
        print('rho_f:', self.rhof)

    def diff(self, x):
        return (self.seFunc(x, taucoef=100))

    def __call__(self, erg, taucoef=100):
        def diff(x):
            return self.diff(x)

        res = derivative(diff, erg, self.DELTA) / self.seFunc.Ef
        print(res)
        return res, None


class DensityOfStatesScipy(DensityOfStates):
    def __init__(self, seFunc):
        DensityOfStates.__init__(self, seFunc)
        self.errors = []

    def diff(self, x):
        se100 = self.seFunc(x, taucoef=100)
        se1 = self.seFunc(x, taucoef=1)
        self.errors.append({
            'tau=100tau0': se100[1],
            'tau=tau0': se1[1]
        })
        return se100[0] - se1[0]

    def __call__(self, erg):
        return DensityOfStates.__call__(self, erg)[0], self.errors
