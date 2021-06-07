import sys
sys.path.append('./tools')
import numpy as np
import matplotlib.pyplot as plt
from derivative import derivative
from integrator import Newton,EPSILON
from math import pi as π

def f(x):
    return x**2
if __name__=='__main__':
    
    X=np.linspace(0,5,100)
    x2der=[derivative(f,x,0,5) for x in X]
    plt.plot(X,x2der)
    plt.show()
