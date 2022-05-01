from tools.physfunction import PhysFunction
import numpy as np
from math import pi


class Altschuler(PhysFunction):
    def __init__(self, taucoef, c=1):
        PhysFunction.__init__(self)
        self.tau = taucoef * self.base_tau0
        self.D = (1 / 3) * self.vf ** 2 * self.tau
        self.l = self.vf * self.tau
        self.rhof = self.rhof * 2
        print(self.rhof)
        self.c = c

    def __call__(self, erg):
        E = erg * self.Ef
        return (
                (
                    -self.ks
                    /
                    (2 * pi ** 2 * self.h * self.D * self.rhof)
                )
                * (
                    np.arctan(
                        self.c
                        /
                        (self.l * self.ks)
                    )
                )
                + (
                        1
                        /
                        (np.sqrt(2) * 4 * pi ** 2 * (self.h * self.D) ** (3 / 2) * self.rhof)
                )
                * np.sqrt(np.abs(E - self.Ef))
        )
