import numpy as np
import matplotlib.pyplot as plt
from integrator import Newton,EPSILON
from math import pi as π 
'''
konstanty


Zakladne konstanty
'''
precision=1e3
#naboj elektronu
e=1.60217662e-19
#htrans
h=1.0545718e-34 
#hmotnost elektronu
m=9.109534e-31 
#fermiho polomer
kf=1.6e10
#fermiho energiay
Ef=(h**2*kf**2)/(2*m)
#tau0
τ0=6.58e-16
#hranica integralu cez q
qmax=10
#permitivita
ε0=8.854187e-12
#tienenie
ks=kf
#bezrozmerna fermiho energia
def selfEnergy(ε,τ=τ0):
    #energia epsilon_tau
    ετ=(h)/(2*τ)
    #bezrozmerna energia
    w=(ε*Ef)/(ετ)
    #bezrozmerna fermiho energia
    uf=(Ef)/(ετ)
    #konstanta pred integralom
    CONST=(e**2*ks)/(8*π**3*ε0)

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
    def integrant(q):
        return ((q**2)/(q**2+1))*F(w,(εq(q*ks))/(ετ))
    prim=[_ for _ in Newton(integrant,EPSILON,qmax,int(precision)).integrate()]
    return CONST*(prim[-1]-prim[0])
    #testovacia self energia
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
    Erg=np.linspace(0.01,1.5,100)
    Σ=np.array([selfEnergy(ε) for ε in Erg])
    Σ5=np.array([selfEnergy(ε,τ=2*τ0) for ε in Erg])
    Σ10=np.array([selfEnergy(ε,τ=5*τ0) for ε in Erg])
    Σtest=np.array([testSelfEnergy(ε) for ε in Erg])
    plt.xlabel(r"$\frac{ε}{E_{Fermi}}$[ 1 ]")
    plt.ylabel(r"$Σ_{self}$ [ J ]")
    plt.xlim(0,1.5)
    plt.plot(Erg,Σtest,linewidth=1,label="analyticka energia")
    plt.plot(Erg,Σ,linewidth=1,label="τ=τ0")
    plt.plot(Erg,Σ5,linewidth=1,label="τ=2τ0")
    plt.plot(Erg,Σ10,linewidth=1,label="τ=5τ0")
    plt.legend() 
    plt.show()
