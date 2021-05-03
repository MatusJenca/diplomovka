import numpy as np
from selfenergy import SelfEnergy
from derivative import derivative
class DensityOfStates:
    def __init__(self,seFunc):
        assert issubclass(type(seFunc),SelfEnergy)
        self.seFunc=seFunc
        self.DELTA=1e-3
    def __call__(self,w,taucoef=100):
        def diff(x):
            return -self.seFunc(x,taucoef=1)+self.seFunc(x,taucoef=taucoef)
        return derivative(diff,w,self.DELTA)
