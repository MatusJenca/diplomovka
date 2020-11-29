import numpy as np
import matplotlib.pyplot as plt
import random
from math import pi
EPSILON=1e-5
#Itegrator class
class Integrator:
    '''
    Integrator class sluzi na krok kroku numericke integrovanie
    '''
    def __init__(self,function,start,end,num):
        '''
           function - to co ideme integrovat
            start, end - hranice
            num - krok, je to to iste ako numpyovske num pri np.linspace (pozri dokumentaciu)
        '''
        self.function=function
        ls=np.linspace(start,end,num,retstep=True)
        '''
        self.samples - xova os pozri numpy.linspace
        self.step - skutocna dlzka kroku
        '''
        self.samples=ls[0]
        self.step=ls[1]
    def intStep(self,x):
        '''
        overridnut funkciou na ratanie kroku napr obdlznikom
        '''
        return
    def integrate(self):
        '''
        generator hodnot primitivnej funkcie
        urcity integral v hraniciach start end dostaneme tak,
        ze z generatora vytvorime zozname
           zoznam=[x for x in instancia.integrate()] 
        a potom
          urcity_integral=zoznam[-1]-zoznam[0]
        '''
        result=0
        for x in self.samples:
            result+=self.intStep(x)
            yield result
#Obdlznikova metoda
class Newton(Integrator):
    def intStep(self,x):
        return ((self.function(x)+self.function(x+self.step))/2)*self.step

'''
Toto uz dat do ineho suboru a importovat
'''

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


