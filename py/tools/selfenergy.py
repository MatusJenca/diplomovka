import numpy as np
from math import pi as pi
from tools.integrator import Newton, EPSILON
from tools.physfunc import PhysFunction


class SelfEnergy(PhysFunction):
    def __init__(self, qmax=None):
        PhysFunction.__init__(self)
        self.uef = (
                (self.Ef * self.h)
                /
                (2 * self.tau0)
        )
        self.qmax = qmax

    def epsilon_tau(self, taucoef):
        return self.h / (2 * self.tau0 * taucoef)

    def function_f(self, x, y):
        def h_arctg(expr):
            return expr * np.arctan(expr)

        f_up1 = h_arctg(x + y + 2 * np.sqrt(x * y) - self.uef)
        f_up2 = h_arctg(x + y - 2 * np.sqrt(x * y) - self.uef)
        f_down1 = h_arctg(x + y + 2 * np.sqrt(x * y))
        f_down2 = h_arctg(x + y - 2 * np.sqrt(x * y))
        func_atan = (-1 / (np.sqrt(4 * x * y))) * (f_up1 - f_up2 - f_down1 - f_down2)
        func_log = 0.5 * (1 / (np.sqrt(4 * x * y))) * (
                np.log(
                    ((x + y + np.sqrt(4 * x * y)) ** 2 - self.uef)
                    /
                    ((x + y - np.sqrt(4 * x * y)) ** 2 - self.uef)
                )
                - np.log(
                    ((x + y + np.sqrt(4 * x * y))**2+1)
                    /
                    ((x + y - np.sqrt(4 * x * y))**2+1)
                )
        )
        return func_atan + func_log

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
        y = (epsilon_q * self.ks ** 2) / self.epsilon_tau(taucoef)
        return const * frac1 * np.sqrt(frac2) * self.function_f(w, y)

    def __call__(self, erg, taucoef=1):
        def podint_f(q):
            return self.integrant(q, w, taucoef)

        w = (erg * self.Ef) / (self.epsilon_tau(taucoef))
        return Newton(podint_f, EPSILON, self.qmax, self.precision).integral_value()

    def test(self, erg):
        k = np.sqrt(
            (2 * self.m * erg * self.Ef)
            /
            (self.h**2)
        )
        const = (
            (self.e**2)
            /
            ((2*pi)**2 * self.permitivity)
            )
        frac = (
            (self.kf**2-k**2 + self.ks**2)
            /
            (4*k)
        )
        ln = np.log(
            ((self.kf + k)**2 + self.ks**2)
            /
            ((self.kf - k)**2 + self.ks**2)
        )
        arc_plus = np.arctan(
            (self.kf + k)
            /
            self.ks
        )
        arc_minus = np.arctan(
            (self.kf - k)
            /
            self.ks
        )
        return 0.5*const * (frac * ln - self.ks * (arc_plus + arc_minus) + self.kf)


