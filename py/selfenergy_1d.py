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
        return np.log((x+y+a+b)**2+1)

    except RuntimeWarning:
        print("Runtime Warning","x:",x,"y:",y,"a:",a,"b:",b)
        return None
#arctg
def F2(x,y,a,b):
    return (x+y+a+b)*np.arctan(x+y+a+b)

#konstanty
#hmotnost elektronu
m0=9.109534e-31
#naboj elektronu
e=1.60217662e-19
#tau
tau0=6.58e-15
#fermiho energia
Efermi=10*e
#fermiho energia uz nanormovana
Uf=200
#fermiho polomer
kf=1.6e10
#katof y
ymax=10
#permitivita vakua
e0=8.8e-12
#reciprocna tieniaca dlzka
ks=kf
#planckova konstanta
hbar=1.0545718e-34
#konstanta pred integralom pri Eself
const=(2*pi)/(2*pi)**3 *(e**2*ks/e0) *(1/pi) *(1/2)
def Y(y):
    citatel=(hbar**2*y**2*ks**2)/(2*m0)
    menovatel=(hbar)/(2*tau0)
    return citatel/menovatel

def F(x,y):
    a=2*np.sqrt(x*y)
    return (1/a)*(F2(x,y,a,-Uf)-F2(x,y,-a,-Uf)-F2(x,y,a,0)+F2(x,y,-a,0)+F1(x,y,a,Uf)-F1(x,y,a,0)-F1(x,y,-a,Uf)+F1(x,y,-a,0))
    
   
def selfEnergy(w):
    def integrant(y):
        return ((y**2)/(1+y**2))*F(w,Y(y))
    integral=[n for n in Newton(integrant,EPSILON,ymax,int(1e2)).integrate()]
    return const*integral[-1]-integral[0]
if __name__=='__main__':
    W=np.linspace(1,2*Uf,100)
    Eself=np.array([selfEnergy(w) for w in W])
    print(Eself)
    plt.plot(W,Eself)
    plt.show()

