import numpy as np
import matplotlib.pyplot as plt
from integrator import Newton,EPSILON
from math import pi as π 
from constants import *


#integrant

#konstanta pred integralom
CONST=(e**2*ks)/(8*π**3*ε0)
#energia epsilon q
def εq(q):
    return (h**2*q**2)/(2*m)

def funkciaPodIntegralom(q,w,ετ):
    '''
    Cela funkcia pod integralom, je rozdelena na casti pretoze je dlha
    '''
    #cast vysledku analytickeho integralu (je to vlastne funkcia bez dosadenia hranic)

    #bezrozmerna fermiho energia
    uf=(Ef)/(ετ)
    def Fpart(x,y,pm,u):
        return 0.5*(np.log((x+y+pm-u)**2+1))+(x+y+pm-u)*np.arctan(x+y+pm-u)
    #vysledok analytickeho integralu
    def F(x,y):
        a=2*np.sqrt(x*y)
        return 1/(a)*((Fpart(x,y,a,uf)-Fpart(x,y,-a,uf))-(Fpart(x,y,a,0)-Fpart(x,y,-a,0)))
    return ((q**2)/(q**2+1))*F(w,(εq(q*ks))/(ετ))
def selfEnergy(ε,τ=τ0,qmax=10):
    #energia epsilon_tau
    ετ=(h)/(2*τ)
    #bezrozmerna energia
    w=(ε*Ef)/(ετ)


    '''
    funkcia pod integralom s konkretnymi parametrami
    '''
    def integrant(q):
        return funkciaPodIntegralom(q,w,ετ)
    '''
    vypocet self enerie
    '''
    #self energia

    prim=[_ for _ in Newton(integrant,EPSILON,qmax,int(precision)).integrate()]
    return CONST*(prim[-1]-prim[0])
    #testovacia self energia

def selfEnergyNoInt(w,τ=τ0,qmax=10): 
    ετ=(h)/(2*τ)
    return CONST*qmax*funkciaPodIntegralom(qmax/2,w,ετ)

def testSelfEnergy(ε):
    k=(np.sqrt(2*m*ε*Ef))/(h)
    C=(e**2)/((2*π)**2*ε0)
    F=(kf**2-k**2+ks**2)/(4*k)
    LN=np.log(((kf+k)**2+ks**2)/((kf-k)**2+ks**2))
    ARC1=(np.arctan((kf+k)/(ks)))
    ARC2=(np.arctan((kf-k)/(ks)))
    return -0.5*C*(F*LN-ks*(ARC1+ARC2)+kf)

'''
telo programu
'''
if __name__=='__main__':
    #hranica integralu cez q
    qmx=1/(τ0*vf)
    qmx=qmx/ks
    print(qmx)

    Erg=np.linspace(0.01,1.5,100)
    Σ=np.array([selfEnergy(ε,qmax=qmx) for ε in Erg])
    Σ100=np.array([selfEnergy(ε,τ=100*τ0,qmax=qmx) for ε in Erg])
    plt.xlabel(r"$\frac{ε}{E_{Fermi}}$[ 1 ]")
    plt.ylabel(r"$Σ_{self}$ [ J ]")
    plt.xlim(0,1.5)
    
    plt.plot(Erg,Σ,linewidth=1,label="τ=τ0")
    plt.plot(Erg,Σ100,linewidth=1,label="τ=$\infty$")
    plt.legend() 
    plt.show()
