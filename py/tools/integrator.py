import numpy as np
import random
from math import pi
EPSILON=1e-10
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
        da sa pouzit na vykreslenie primitivnej funkcie 
        plt.plot(self.samples,[_ for _ in self.integrate])
        '''
        result=0
        for x in self.samples:
            st=self.intStep(x)
            result+=st
            yield result
    def integral_value(self,mindist=1):
        '''
        urcity integral v hraniciach, ale ignorujeme hodnoty pokial su nan
        da sa nastavit maximalna vzdialenost hodnot v pocte samplov
        '''
        prim = [_ for _ in self.integrate()]
        ia=0
        a=prim[ia]
        for i,x in enumerate(prim):
            if str(x)!='nan':
                ia=i
                a=x
                break
        ib=len(prim)-1
        b=prim[-1]
        for i,x in enumerate(prim[::-1]):
            if str(x)!='nan':
                ib=len(prim)-i-1
                b=x
                break
        if abs(ia-ib)>=mindist:
            return b-a
        else:
            raise ValueError("too few valid samples to compute integral")
      
                
            
            
        
#Obdlznikova metoda
class Newton(Integrator):
    def intStep(self,x):
        res=((self.function(x)+self.function(x+self.step))/2)*self.step
        return res
