import numpy as np
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
            st=self.intStep(x)
            result+=st
            yield result
#Obdlznikova metoda
class Newton(Integrator):
    def intStep(self,x):
        return ((self.function(x)+self.function(x+self.step))/2)*self.step