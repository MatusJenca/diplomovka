import numpy as np
from math import pi as π 
from integrator import Newton, EPSILON
from physfunc import PhysFunction

        
        
class SelfEnergy(PhysFunction):
    def __init__(self, τ0=6.58e-15,qmax=None):
        PhysFunction.__init__(self)

    def __call__(self,ε,taucoef=1):
        pass
    def test(self,ε):
        k=(np.sqrt(2*self.m*ε*self.Ef))/(self.h)
        C=(self.e**2)/((2*π)**2*self.ε0)
        F=(self.kf**2-k**2+self.ks**2)/(4*k)
        LN=np.log(((self.kf+k)**2+self.ks**2)/((self.kf-k)**2+self.ks**2))
        ARC1=(np.arctan((self.kf+k)/(self.ks)))
        ARC2=(np.arctan((self.kf-k)/(self.ks)))
        return 0.5*C*(F*LN-self.ks*(ARC1+ARC2)+self.kf)

