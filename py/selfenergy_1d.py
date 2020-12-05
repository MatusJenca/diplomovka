import numpy as np
import matplotlib.pyplot as plt
from integrator import Newton,EPSILON
from math import pi as π 
'''
konstanty


Zakladne konstanty
'''
precision=1e2
#naboj elektronu
e=1.60217662e-19
#htrans
h=1.0545718e-34 
#hmotnost elektronu
m=9.109534e-31 
#fermiho energia
Ef=10*e
#fermiho polomer
kf=1.6*10e10
#tau0
τ0=6.58e-15
#hranica integralu cez q
qmax=10
#permitivita
ε0=8.854187e-12

'''
Odvodene konstanty
'''
#tau
τ=τ0
#tienenie
ks=kf
#energia epsilon_tau
ετ=(h)/(2*τ)
#bezrozmerna fermiho energia
uf=(Ef)/(ετ)
#konstanta pred integralom
CONST=(e**2*ks)/(π**3*ε0)

'''
Pomocne funkcie
'''
#energia epsilon q
def εq(q):
    return (h**2*q**2)/(2*m)
#cast vysledku analytickeho integralu (je to vlastne funkcia bez dosadenia hranic)
def Fpart(x,y,pm,u):
    return 0.5*(np.log((x+y+pm-u)**2+1))+(x+y+pm-u)*np.arctan(x+y+pm-u)
#vysledok analytickeho integralu
def F(x,y):
    a=2*np.sqrt(x*y)
    return 1/(a)*((Fpart(x,y,a,uf)-Fpart(x,y,-a,uf))-(Fpart(x,y,a,0)-Fpart(x,y,-a,0)))
'''
vypocet self enerie
'''
#self energia
def selfEnergy(w):
    def integrant(q):
        return ((q**2)/(q**2+1))*F(w,(εq(q*ks))/(ετ))
    prim=[_ for _ in Newton(integrant,EPSILON,qmax,int(precision)).integrate()]
    return CONST*(prim[-1]-prim[0])
#testovacia self energia
def testSelfEnergy(w):
    k=(np.sqrt(2*m*ετ*w))/(h)
    C=(e**2)/((2*π)**3)
    F=(kf**2-k**2+ks**2)/(4*k)
    LN=np.log(((kf+k)**2+ks**2)/((kf-k)**2+ks**2))
    ARC1=(np.arctan((kf+k)/(ks)))
    ARC2=(np.arctan((kf-k)/(ks)))
    return -C*F*LN-ks*(ARC1+ARC2)+kf

    

'''
telo programu
'''
if __name__=='__main__':
    print('τ',τ)
    print('ks',ks)
    print('ετ',ετ)
    print('uf',uf)
    print('CONST',CONST)
    W=np.linspace(10,2*uf,100)
    Σ=np.array([selfEnergy(w) for w in W])
    Σtest=np.array([testSelfEnergy(w) for w in W])
    plt.plot(W,Σ)
    #plt.plot(W,Σtest)
    plt.show()

