import numpy as np
from math import pi

class PhysFunction:
    def __init__(self):
        self.precision = int(1e3)
        # naboj elektronu
        self.e = 1.60217662e-19
        # htrans
        self.h = 1.0545718e-34
        # hmotnost elektronu
        self.m = 9.109534e-31  # fermiho polomer
        self.kf = 1.6e10
        # tienenie
        self.ks = self.kf
        # fermiho energia
        self.Ef = (self.h ** 2 * self.kf ** 2) / (2 * self.m)
        print(self.Ef / self.e)
        # fermiho rychlost
        self.vf = np.sqrt((2 * self.Ef) / self.m)
        # hustotastavov na fermiho energii
        self.rhof = (
                0.5 * (
                    1
                    /
                    (2*pi**2)
                )
                *
                (
                    (2*self.m)
                    /
                    (self.h**2)
                )**(3/2)
                * np.sqrt(self.Ef)
        )
        # permitivita
        self.perm = 8.854187e-12
        # zakladne tau 0
        self.base_tau0 = 6.58e-15