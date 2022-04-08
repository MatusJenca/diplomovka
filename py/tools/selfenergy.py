import numpy as np
from math import pi as pi
from tools.integrator import Newton, EPSILON
from tools.physfunc import PhysFunction


class SelfEnergy(PhysFunction):
    def __init__(self, qmax=None):
        PhysFunction.__init__(self)
        self.uef = (
            (self.Ef*self.h)
            /
            (2 * self.tau0)
        )
        self.qmax = qmax

    def epsilon_tau(self, taucoef):
        return self.h / (2 * self.tau0 * taucoef)

    def function_f(self, x, y):
        def h_arctg(expr):
            return expr * np.arctan(expr)
        # Arcustangens
        arctg = (
                h_arctg(x + y + 2 * np.sqrt(x * y) - self.uef)
                - h_arctg(x + y - 2 * np.sqrt(x * y) - self.uef)
                - h_arctg(x + y + 2 * np.sqrt(x * y))
                + h_arctg(x + y - 2 * np.sqrt(x * y))
        )
        # Logaritmus
        numerator_left = (x + y + 2 * np.sqrt(x * y) - self.uef) ** 2 + 1
        denominator_left = (x + y - 2 * np.sqrt(x * y) - self.uef) ** 2 + 1
        numerator_right = (x + y - 2 * np.sqrt(x * y)) ** 2 + 1
        denominator_right = (x + y + 2 * np.sqrt(x * y)) ** 2 + 1
        frac_left = numerator_left / denominator_left
        frac_right = numerator_right / denominator_right
        log = np.log(frac_left * frac_right)
        # vysledna funkcia
        return (1 / np.sqrt(4 * x * y)) * (arctg - 0.5 * log)

    def integrant(self, q, w, taucoef):
        const = (
                (self.e ** 2)
                /
                (8 * pi ** 4 * self.permitivity * self.ks ** (-1))
        )
        frac1 = (
                (q ** 2)
                /
                (1 + q ** 2)
        )
        frac2 = (
                self.epsilon_tau(taucoef)
                /
                self.Ef
        )
        epsilon_q = (
                (self.h ** 2 * q ** 2)
                /
                (2 * self.m)
        )
        y = (epsilon_q * self.ks**2) / self.epsilon_tau(taucoef)
        return const * frac1 * np.sqrt(frac2) * self.function_f(w, y)

    def __call__(self, erg, taucoef=1):
        def podint_f(q):
            return self.integrant(q, w, taucoef)

        w = (erg * self.Ef) / (self.epsilon_tau(taucoef))
        print(w)
        return Newton(podint_f, EPSILON, self.qmax, self.precision).integral_value()

    def test(self, erg):
        k = (np.sqrt(2 * self.m * erg * self.Ef)) / (self.h)
        C = (self.e ** 2) / ((2 * pi) ** 2 * self.permitivity)
        F = (self.kf ** 2 - k ** 2 + self.ks ** 2) / (4 * k)
        LN = np.log(((self.kf + k) ** 2 + self.ks ** 2) / ((self.kf - k) ** 2 + self.ks ** 2))
        ARC1 = (np.arctan((self.kf + k) / (self.ks)))
        ARC2 = (np.arctan((self.kf - k) / (self.ks)))
        return 0.5 * C * (F * LN - self.ks * (ARC1 + ARC2) + self.kf)
