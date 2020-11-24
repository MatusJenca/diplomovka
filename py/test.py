import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append(".")
from integrator import Newton, EPSILON

class Testovic:
	def __init__(self,funkcia,interval=(0,10),num=100):
		self.test=Newton(funkcia,interval[0],interval[1],num)
		self.interval=interval
	def testujHodnotu(self,exp_val):
		prim=[x for x in self.test.integrate()]
		real_val=prim[-1]-prim[0]
		print("Funkcia:",self.test.function.__name__,"Interval:",self.interval,"Ocakavana hodnota:",exp_val,"Skutocna hodnota",real_val,sep="\n")
	def testujGraf(self,uloz=True):
		X=self.test.samples
		Y=[y for y in self.test.integrate()]
		plt.plot(X,Y,label=self.test.function.__name__)
		if uloz:
			plt.savefig(self.test.function.__name__+"_"+str(self.interval[0])+"_"+str(self.interval[1]))
		else:
			plt.show()
		
def x2(x):
    return x**2
tx2=Testovic(x2,num=10000)
tsin=Testovic(np.sin,num=int(1e4))
tcos=Testovic(np.cos,num=int(1e4))
tlog=Testovic(np.log,num=int(1e4))
tatan=Testovic(np.arctan,num=int(1e4))
tx2.testujHodnotu(333.33)
tx2.testujGraf()
tsin.testujHodnotu(1.8391)
tsin.testujGraf()
tcos.testujHodnotu(-0.54402)
tcos.testujGraf()
tlog.testujHodnotu(13.026)
tlog.testujGraf()
tatan.testujHodnotu(12.4037)
tatan.testujGraf()
