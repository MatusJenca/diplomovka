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
        Ui=(
            (self.e**2)
            /
            (4*pi**self.perm*self.ks**(-1))
        )
        Uco=2*self.h*self.D*self.ks**2
        return (
                (
                    (4*Ui)
                    /
                    (pi**2*Uco*self.l*self.ks)
                )
                +
                (
                    (2*Ui)
                    /
                    (pi*Uco*np.sqrt(2*self.h*self.D*self.ks**2))
                )
                * np.sqrt(np.abs(E-self.Ef))
            )

