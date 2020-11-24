import sys
sys.path.append(".")
from integrator import Newton,EPSILON
import numpy as np
import matplotlib.pyplot as plt
from math import pi
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
#fermiho energia uz nanormovana
Ef=200
#fermiho polomer
kf=1.6e10
#katof y
ymax=1/200
#permitivita vakua
e0=8.8e-12
#hmotnost elektronu
m0=9.109534e-31
#naboj elektronu
e=1.60217662e-19
#reciprocna tieniaca dlzka
ks=kf
#konstanta pred integralom pri Eself
const=(e**2)/(2*pi**4*e0*ks)

def F(x,y):
    a=2*np.sqrt(x*y)
    return (1/a)*(F2(x,y,a,-Ef)-F2(x,y,-a,-Ef)-F2(x,y,a,0)+F2(x,y,-a,0)+F1(x,y,a,Ef)-F1(x,y,a,0)-F1(x,y,-a,Ef)+F1(x,y,-a,0))
    
   
def selfEnergy(w):
    def integrant(y):
        return ((y**2)/(1+y**2))*F(w,y)
    integral=[n for n in Newton(integrant,EPSILON,ymax,100).integrate()]
    return const*integral[-1]-integral[0]
#vytvor linspace pre w
W=np.linspace(1,2*Ef,100)
Eself=np.array([selfEnergy(w) for w in W])
print(Eself)
plt.plot(W,Eself)
plt.show()
