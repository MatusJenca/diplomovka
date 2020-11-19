import sys
sys.path.append(".")
from integrator import Newton,EPSILON
import numpy as np
import matplotlib.pyplot as plt
'''
#Ked dostavam runtime warningy
import warnings
warnings.filterwarnings("error")
'''

#funkcie
#log
def F1(x,y,a,b):
    try:    
        return np.log(x+y+a+b)

    except RuntimeWarning:
        print("Runtime Warning","x:",x,"y:",y,"a:",a,"b:",b)
        return None
#arctg
def F2(x,y,a,b):
    return (x+y+a+b)*np.arctan(x+y+a+b)

#konstanty
Ef=200
ymax=1/200
e0=8.8e-12
m0=1
const=1

def F(x,y):
    a=2*np.sqrt(x*y)
    return (1/a)*(F2(x,y,a,-Ef)-F2(x,y,-a,-Ef)-F2(x,y,a,0)+F2(x,y,-a,0)+F1(x,y,a,Ef)-F1(x,y,a,0)-F1(x,y,-a,Ef)+F1(x,y,-a,0))
    
   
def selfEnergy(w):
    def integrant(y):
        return ((y**2)/(1+y**2))*F(w,y)
    integral=[n for n in Newton(integrant,EPSILON,ymax,100).integrate()]
    return const*integral[-1]-integral[0]
#vytvor linspace pre w
W=np.linspace(1,10,10)
Eself=np.array([selfEnergy(w) for w in W])
print(Eself)
plt.plot(W,Eself)
plt.show()
