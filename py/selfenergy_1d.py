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
#tau0
tau0=6.58e-15
#tau
tau=tau0
#fermiho energia
Efermi=10*e
#fermiho energia uz nanormovana
Uf=200
#fermiho polomer
kf=1.6e10
#reciprocna tieniaca dlzka
ks=kf
#qmax
qmax=10*ks
#permitivita vakua
e0=8.8e-12
#planckova konstanta
hbar=1.0545718e-34
#epsilon_tau
et=hbar/(2*tau)
#konstanta pred integralom pri Eself
const=(2*pi)/(2*pi)**3 *(e**2*ks/e0) *(1/pi) *(1/2)
def Y(q):
    return (hbar**2*q**2)/(2*m0*et)

def F(x,y):
    a=2*np.sqrt(x*y)
    return (1/a)*(F2(x,y,a,-Uf)-F2(x,y,-a,-Uf)-F2(x,y,a,0)+F2(x,y,-a,0)+F1(x,y,a,Uf)-F1(x,y,a,0)-F1(x,y,-a,Uf)+F1(x,y,-a,0))
    
   
def selfEnergy(w):
    def integrant(q):
        return ((q**2)/(ks**2+q**2))*F(w,Y(q))
    integral=[n for n in Newton(integrant,EPSILON,qmax,int(1e2)).integrate()]
    print(w)
    return const*integral[-1]-integral[0]
if __name__=='__main__':
    W=np.linspace(1,2*Uf,100)
    Eself=np.array([selfEnergy(w) for w in W])
    plt.plot(W,Eself)
    plt.show()
