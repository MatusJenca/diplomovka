import numpy as np
from math import pi as π 
from derivative import derivative
from selfenergy import PhysFunction
from integrator import Newton,EPSILON

class Sigma(PhysFunction):
    #ωρετ
    def __init__(self,τ,corr=False):
        PhysFunction.__init__(self)
        self.corr=corr
        self.τ=τ
        C1=(((2*self.m)/(self.h**2))**(3/2))/(2*π**2)
        C2=(2*self.m)/(2*self.h**2)
        self.CONST=(C1*C2)/(self.rhof*self.kf**2)
        print(self.CONST)
    def podint_f(self,ε,ω):
            return ε**(3/4)*(ε+self.h*ω)**(3/4)
    def F(self,ω):
        res=[]
        for value in ω:        
            def integrant(ε):
                return self.podint_f(ε,value)
            intv=Newton(integrant,self.Ef-self.h*value,self.Ef,self.precision).integral_value()
            res.append((self.CONST*intv)/(self.h*value))
        return np.array(res)
        
    def __call__(self,ω):
        no_corr=(self.e**2*self.h**2*self.kf**2*self.τ*self.rhof)/(3*self.m**2*(1+self.τ**2*ω**2))
        if not self.corr:
            return no_corr
        else:
            #return self.F(ω)
            return no_corr*self.F(ω)
class TestF(Sigma):
    def __init__(self,ω):
        Sigma.__init__(self,6.58e-16,False)
        self.ω=ω
    def __call__(self,ε):
        return self.integrant(ε,self.ω)
        
    
        
        