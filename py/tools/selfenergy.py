import numpy as np
from math import pi as π
from tools.integrator import Newton, EPSILON


class PhysFunction:
    def __init__(self):
        self.precision = int(1e3)
        # naboj elektronu
        self.e = 1.60217662e-19
        # htrans
        self.h = 1.0545718e-34
        # hmotnost elektronu
        self.m = 9.109534e-31
        # fermiho polomer
        self.kf = 1.6e10
        # tienenie
        self.ks = self.kf
        # fermiho energia
        self.Ef = (self.h ** 2 * self.kf ** 2) / (2 * self.m)
        print(self.Ef)
        # fermiho rychlost
        self.vf = np.sqrt((2 * self.Ef) / self.m)
        # hustotastavov na fermiho energii
        self.rhof = ((self.m / self.h ** 2) ** (3 / 2) * self.Ef ** (1 / 2)) / (2 * π ** 2)
        # permitivita
        self.perm = 8.854187e-12
        # zakladne tau 0
        self.base_tau0 = 6.58e-15


class SelfEnergy(PhysFunction):
    def __init__(self, tau0=6.58e-15, qmax=None):
        PhysFunction.__init__(self)
        # tau0
        self.tau0 = tau0
        # hranica integralu
        if qmax == None:
            qmx = 1 / (self.tau0 * self.vf)
            self.qmax = qmx / self.ks
        else:
            self.qmax = qmax
        # konstanta pred integralom
        self.CONST = (self.e ** 2 * self.ks) / (8 * π ** 3 * self.perm)

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
        return ((q ** 2) / (q ** 2 + 1)) * self.F(w, self.epsilon_q(q * self.ks) / (epsilon_tau), epsilon_tau, uf)

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
        return self.CONST * (prim[-1] - prim[0])
        # testovacia self energia

    def test(self, erg):
        k = (np.sqrt(2 * self.m * erg * self.Ef)) / (self.h)
        C = (self.e ** 2) / ((2 * π) ** 2 * self.perm)
        F = (self.kf ** 2 - k ** 2 + self.ks ** 2) / (4 * k)
        LN = np.log(((self.kf + k) ** 2 + self.ks ** 2) / ((self.kf - k) ** 2 + self.ks ** 2))
        ARC1 = (np.arctan((self.kf + k) / (self.ks)))
        ARC2 = (np.arctan((self.kf - k) / (self.ks)))
        return 0.5 * C * (F * LN - self.ks * (ARC1 + ARC2) + self.kf)
