import numpy as np
from  selfenergy_1d import F1,F2
Uf=1
def testF1(x,y):
    a=2*np.sqrt(x*y)
    return (1/a)*(F1(x,y,a,Uf)-F1(x,y,a,0)-F1(x,y,-a,Uf)+F1(x,y,-a,0))

