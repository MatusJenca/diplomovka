import numpy as np
from math import pi
from tools.integrator import Newton, DoubleNewton, EPSILON
from tools.physfunction import PhysFunction
from scipy.integrate import quad, dblquad


class SelfEnergy(PhysFunction):
    def __init__(self, tau0=6.58e-15, qmax=None):
        PhysFunction.__init__(self)
        # tau0
        self.tau0 = tau0
        # hranica integralu
        if qmax is None:
            qmx = 1 / (self.tau0 * self.vf)
            self.qmax = qmx / self.ks
        else:
            self.qmax = qmax
        # konstanta pred integralom
        self.CONST = (self.e ** 2 * self.ks) / (8 * pi ** 3 * self.perm)

    def epsilon_q(self, q):
        return (self.h ** 2 * q ** 2) / (2 * self.m)

    def log(self, x, y, pm, u):
        return 0.5 * (np.log((x + y + pm - u) ** 2 + 1))

    def atan(self, x, y, pm, u):
        return (x + y + pm - u) * np.arctan(x + y + pm - u)

    # testovacie funkcie
    def fup1(self, x, y, uf):
        return self.atan(x, y, 2 * np.sqrt(x * y), uf)

    def fup2(self, x, y, uf):
        return self.atan(x, y, -2 * np.sqrt(x * y), uf)

    def fdown1(self, x, y):
        return self.atan(x, y, 2 * np.sqrt(x * y), 0)

    def fdown2(self, x, y):
        return self.atan(x, y, -2 * np.sqrt(x * y), 0)

    def funcAtan(self, x, y, uf):
        return (-1 / (np.sqrt(4 * x * y))) * (
                (self.fup1(x, y, uf) - self.fup2(x, y, uf)) - (self.fdown1(x, y) - self.fdown2(x, y)))

    def funcLog(self, x, y, uf):
        # print(x, y, uf, sep="\t")
        return 0.5 * ((1) / (np.sqrt(4 * x * y))) * (np.log(
            ((x + y + np.sqrt(4 * x * y) - uf) ** 2 + 1) / ((x + y - np.sqrt(4 * x * y) - uf) ** 2 + 1)) - np.log(
            ((x + y + np.sqrt(4 * x * y)) ** 2 + 1) / ((x + y - np.sqrt(4 * x * y)) ** 2 + 1)))

    def Fpart(self, x, y, pm, u):
        return self.log(x, y, pm, u) + self.atan(x, y, pm, u)

    def F(self, x, y, epsilon_tau, uf):
        a = 2 * np.sqrt(x * y)
        # return 1/(a)*((self.Fpart(x,y,a,uf)-self.Fpart(x,y,-a,uf))-(self.Fpart(x,y,a,0)-self.Fpart(x,y,-a,0))) #to povodne
        return self.funcAtan(x, y, uf) + self.funcLog(x, y, uf)  # to z fortranu
        # return (1/(a))*(self.log(x,y,a,uf)-self.atan(x,y,a,uf)-self.log(x,y,a,0)-self.atan(x,y,a,0)-self.log(x,y,-a,uf)+self.atan(x,y,-a,uf)+self.log(x,y,-a,0)+self.atan(x,y,-a,0)) #zo zosita

    def funkciaPodIntegralom(self, q, w, epsilon_tau):
        """
        Cela funkcia pod integralom, je rozdelena na casti pretoze je dlha
        """

        # bezrozmerna fermiho energia
        uf = (self.Ef) / (epsilon_tau)
        # vysledok analytickeho integralu
        return self.CONST * ((q ** 2) / (q ** 2 + 1)) * self.F(w, self.epsilon_q(q * self.ks) / (epsilon_tau),
                                                               epsilon_tau, uf)

    def __call__(self, erg, taucoef=1):
        # tau
        tau = taucoef * self.tau0
        # energia epsilon_tau
        epsilon_tau = (self.h) / (2 * tau)
        # bezrozmerna energia
        w = (erg * self.Ef) / (epsilon_tau)

        '''
        funkcia pod integralom s konkretnymi parametrami
        '''

        def integrant(q):
            return self.funkciaPodIntegralom(q, w, epsilon_tau)

        '''
        vypocet self enerie
        '''
        # self energia

        prim = [_ for _ in Newton(integrant, EPSILON, self.qmax, int(self.precision)).integrate()]
        return prim[-1] - prim[0]
        # testovacia self energia

    def test(self, erg):
        k = (np.sqrt(2 * self.m * erg * self.Ef)) / (self.h)
        C = (self.e ** 2) / ((2 * pi) ** 2 * self.perm)
        F = (self.kf ** 2 - k ** 2 + self.ks ** 2) / (4 * k)
        LN = np.log(((self.kf + k) ** 2 + self.ks ** 2) / ((self.kf - k) ** 2 + self.ks ** 2))
        ARC1 = (np.arctan((self.kf + k) / (self.ks)))
        ARC2 = (np.arctan((self.kf - k) / (self.ks)))
        return 0.5 * C * (F * LN - self.ks * (ARC1 + ARC2) + self.kf)


df = 0


class DoubleSelfEnergy(SelfEnergy):
    def funkciaPodIntegralom(self, x, y, w, epsilon_tau):
        uf = self.Ef / epsilon_tau
        return (
                (
                        1
                        /
                        ((2 * pi) ** 3 * pi ** 2)
                )
                *
                (
                        (2 * pi * self.e ** 2)
                        /
                        (self.perm * self.ks ** (-1))
                )
                *
                (
                        1
                        /
                        np.sqrt(w)
                )
                *
                (
                        np.sqrt(x)
                        /
                        ((w - x) ** 2 + 1)
                )
                *
                (
                        (y ** 2)
                        /
                        (y ** 2 + 1)
                )
                * self.F(x,
                         (self.h ** 2 * self.ks ** 2 * y ** 2)
                         /
                         (2 * self.m * epsilon_tau)
                         , epsilon_tau, uf)

        )

    def __call__(self, erg, taucoef=1):
        print(f"computing 2d integral for: E = {erg}")
        # tau
        tau = taucoef * self.tau0
        # energia epsilon_tau
        epsilon_tau = self.h / (2 * tau)
        # bezrozmerna energia
        w = (erg * self.Ef) / (epsilon_tau)

        def integrant(x, q):
            return self.funkciaPodIntegralom(x, q, w, epsilon_tau)

        start = np.array(2 * [EPSILON])
        end = np.array([self.Ef+30*epsilon_tau, self.qmax])
        num = np.array([int(2e4), int(1e3)])
        ret = DoubleNewton(integrant, start, end, num).integral_value()
        print(ret)
        return ret


class SelfEnergyScipy(SelfEnergy):
    def __call__(self, erg, taucoef=1):
        # tau
        tau = taucoef * self.tau0
        # energia epsilon_tau
        epsilon_tau = (self.h) / (2 * tau)
        # bezrozmerna energia
        w = (erg * self.Ef) / (epsilon_tau)
        return quad(
            self.funkciaPodIntegralom,
            a=0,
            b=self.qmax,
            args=(w, epsilon_tau),
            epsabs=1e-30,
            epsrel=1e-20
        )


class DoubleSelfEnergyScipy(DoubleSelfEnergy):
    def __call__(self, erg, taucoef=1):
        # tau
        tau = taucoef * self.tau0
        # energia epsilon_tau
        epsilon_tau = (self.h) / (2 * tau)
        # bezrozmerna energia
        w = (erg * self.Ef) / (epsilon_tau)
        print(f"computing 2d integral for: E = {erg}")
        print(f"tau = {tau} , qmax ={self.qmax}")
        ret = dblquad(self.funkciaPodIntegralom,
                      args=(w, epsilon_tau),
                      a=0,
                      b=np.inf,
                      gfun=lambda x: 0,
                      hfun=lambda x: self.qmax,
                      epsabs=1e-30
                      )
        print(ret)
        return ret
