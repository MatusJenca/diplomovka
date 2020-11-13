import numpy as np
import matplotlib.pyplot as plt
from math import pi
class Integrator:
    def __init__(self,function,start,end,num):
        self.function=function
        ls=np.linspace(start,end,num,retstep=True)
        self.samples=ls[0]
        self.step=ls[1]
    def intStep(self,x):
        return
    def integrate(self):
        result=0
        for x in self.samples:
            result+=self.intStep(x)
            yield result

class Newton(Integrator):
    def intStep(self,x):
        return ((self.function(x)+self.function(x+self.step))/2)*self.step
#TEST
'''
test=Newton(lambda x: x,0,20,50)
Y=np.array([y for y in test.integrate()])
plt.plot(np.array(test.samples),Y)
plt.show()
'''
#funkcie
#log
def F1(x,y,a,b):
    return np.log(x+y+a+b)
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
    integral=[n for n in Newton(integrant,0,ymax,100).integrate()]
    return const*integral[-1]-integral[0]
W=np.linspace(1,10,10)
E=np.array([selfEnergy(w) for w in W])
print(E)

