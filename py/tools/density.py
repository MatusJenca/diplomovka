import numpy as np
from selfenergy import SelfEnergy
from derivative import derivative
from integrator import Newton,EPSILON
class DensityOfStates:
    def __init__(self,seFunc):
        assert issubclass(type(seFunc),SelfEnergy)
        self.seFunc=seFunc
        self.DELTA=1e-3
    def __call__(self,ε,taucoef=100):
        ετ0=(self.seFunc.h)/(2*self.seFunc.τ0)
        ετ=(self.seFunc.h)/(2*self.seFunc.τ0*taucoef)
        def diff(x):
            return self.seFunc(x,taucoef=100) - self.seFunc(x,taucoef=1)
        #return diff(ε)/self.seFunc.Ef
        res=derivative(diff,ε,self.DELTA)/self.seFunc.Ef
        print(res)
        return res
class DOSDirect(SelfEnergy):
    def __init__(self,τ0=6.58e-16,qmax=None):
        SelfEnergy.__init__(self,τ0,qmax)
    def FpartDer(self,x,y,plus,u):
        a=np.sqrt(x*y)
        b=(y)/(a)
        if plus:
            zlomok1=((b+1)*(-u+2*a+x+y))/((u-2*a-x-y)**2+1)
            zlomok2=((-b-1)*(-u+2*a+x+y))/((-u+2*a+x+y)**2+1)
            return zlomok1 - zlomok2 - (b+1)*np.arctan(u-2*a-x-y)
        zlomok1=((b-1)*(-u-2*a+x+y))/((-u-2*a+x+y)**2+1)
        zlomok2=((1-b)*(-u-2*a+x+y))/((u+2*a-x-y)**2+1)
        return -zlomok1 + zlomok2 - (1-b)*np.arctan(u+2*a-x-y)
    def F(self,x,y,ετ,uf):
        a=2*np.sqrt(x*y)
        b=-y/(4*pow(x*y,3/2))
        return (b*((self.Fpart(x,y,a,uf)-self.Fpart(x,y,-a,uf))-(self.Fpart(x,y,a,0)-self.Fpart(x,y,-a,0)))+1/(a)*((self.FpartDer(x,y,True,uf)-self.FpartDer(x,y,False,uf))-(self.FpartDer(x,y,True,0)-self.FpartDer(x,y,False,0))))/ετ
    def __call__(self,ε):
        ετ0=(self.h)/(2*self.τ0)
        w0=(ε*self.Ef)/(ετ0)
        τ=100*self.τ0
        ετ=(self.h)/(2*τ)
        w=(ε*self.Ef)/(ετ)
        def integrant0(q):
            return self.funkciaPodIntegralom(q,w0,ετ0)
        def integrant(q):
            return self.funkciaPodIntegralom(q,w,ετ)
        prim0=[_ for _ in Newton(integrant0,EPSILON,self.qmax,int(self.precision)).integrate()] 
        prim=[_ for _ in Newton(integrant,EPSILON,self.qmax,int(self.precision)).integrate()]
        #return self.CONST*self.Ef*(-(prim0[-1]-prim0[0])/ετ0+(prim[-1]-prim[0])/ετ)
        return -self.CONST*((prim0[-1]-prim0[0])-(prim[-1]-prim[0]))
class DOSDirectNoInt(DOSDirect):
    def __init__(self,τ0=6.58e-16,qmax=None):
        DOSDirect.__init__(self,τ0,qmax)
    def __call__(self,ε): 
        ετ0=(self.h)/(2*self.τ0)
        w0=(ε*self.Ef)/(ετ0)
        τ=100*self.τ0
        ετ=(self.h)/(2*τ)
        w=(ε*self.Ef)/(ετ)
        return -self.qmax*(self.funkciaPodIntegralom(self.qmax/2,w0,ετ0))+self.qmax*(self.funkciaPodIntegralom(self.qmax/2,w,ετ))
