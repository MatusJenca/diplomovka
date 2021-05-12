import numpy as np
from selfenergy import SelfEnergy
from derivative import derivative
from integrator import Newton,EPSILON
class DensityOfStates:
    def __init__(self,seFunc):
        assert issubclass(type(seFunc),SelfEnergy)
        self.seFunc=seFunc
        self.DELTA=1e-3
    def __call__(self,w,taucoef=100):
        def diff(x):
            return -self.seFunc(x,taucoef=1)+self.seFunc(x,taucoef=taucoef)
        return derivative(diff,w,self.DELTA)
class DOSDirect(SelfEnergy):
    def __init__(self,τ0=6.58e-16,qmax=None):
        SelfEnergy.__init__(self,τ0,qmax)
    def Fpart(self,x,y,pm,u):
        return 3*(pm-u+x+y)/((pm-u+x+y)**2+1) + np.arctan(x+y+pm-u)
    def __call__(self,ε):
        ετ0=(self.h)/(2*self.τ0)
        w0=(ε*self.Ef)/(ετ0)
        ετ=ετ0/100
        w=100*w0
        def integrant0(q):
            return self.funkciaPodIntegralom(q,w0,ετ0)
        def integrant(q):
            return self.funkciaPodIntegralom(q,w,ετ)
        prim0=[_ for _ in Newton(integrant0,EPSILON,self.qmax,int(self.precision)).integrate()] 
        prim=[_ for _ in Newton(integrant,EPSILON,self.qmax,int(self.precision)).integrate()]
        return self.CONST*(-(prim0[-1]-prim0[0])+(prim[-1]-prim[0]))
class DOSDirectNoInt(DOSDirect):
    def __init__(self,τ0=6.58e-16,qmax=None):
        DOSDirect.__init__(self,τ0,qmax)
    def __call__(self,ε):
        ετ0=(self.h)/(2*self.τ0)
        w0=(ε*self.Ef)/(ετ0)
        ετ=ετ0/100
        w=100*w0
        return -(1/(self.vf*self.τ0))*(self.funkciaPodIntegralom(EPSILON,w0,ετ0))+(1/(self.vf*self.τ0))*(self.funkciaPodIntegralom(EPSILON,w,ετ))
