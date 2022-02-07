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
        
    def ρ(self,ε):          
        return (((2*self.m)/(self.h**2))**(2/3)*np.sqrt(ε))/(2*π**2)
    def k(self,ε):
        return (np.sqrt(2*self.m*ε))/(self.h)
    def integrant(self,ε,ω):
        try:
            ε=ε.clip(min=EPSILON)
        except AttributeError:
            if ε<=0:
                print("jebem to do huby")
                ε=EPSILON
        hω=self.h*ω
        res=(self.ρ(ε)**0.5*self.k(ε)*self.ρ(ε+hω)**0.5*self.k(ε+hω))/(self.ρ(self.Ef)*self.kf)

        return res
    def F(self,ω):
        def poddint_f(ε):
            return self.integrant(ε,ω)    
        hω=self.h*ω
        return Newton(poddint_f,10,100,int(self.precision)).integral_value()
    def __call__(self,ω):
        hω=self.h*ω
        nocorr=(self.e**2*self.h**2*self.kf**2*self.τ*self.ρ(self.Ef))/(3*self.m**2*(1+self.τ**2*ω**2))
        if not self.corr:
            return nocorr
        return  self.F(ω)
class TestF(Sigma):
    def __init__(self,ω):
        Sigma.__init__(self,6.58e-16,False)
        self.ω=ω
    def __call__(self,ε):
        return self.integrant(ε,self.ω)
        
    
        
        