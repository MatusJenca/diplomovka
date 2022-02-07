import sys
sys.path.append('tools')
import numpy as np
import matplotlib.pyplot as plt
from sigma import Sigma,TestF
from integrator import Newton,EPSILON
if __name__=="__main__": 

    sigmafunc_nocorr=Sigma(τ=6.58e-16)
    sigmafunc=Sigma(τ=6.58e-16,corr=True)
    ω=(np.linspace(EPSILON,1,100)*sigmafunc_nocorr.Ef)/sigmafunc_nocorr.h
    
    #σ0=sigmafunc_nocorr(ω)
    #σ=sigmafunc(ω)

    #TEST
    ω1=(0.1*sigmafunc_nocorr.Ef)/sigmafunc_nocorr.h
    ω2=(0.25*sigmafunc_nocorr.Ef)/sigmafunc_nocorr.h
    ω3=(0.5*sigmafunc_nocorr.Ef)/sigmafunc_nocorr.h
    ω4=(sigmafunc_nocorr.Ef)/sigmafunc_nocorr.h
    testfunc1=TestF(ω1)
    testfunc2=TestF(ω2)
    testfunc3=TestF(ω3)
    testfunc4=TestF(ω4)
    print( ω1, ω2, ω3, ω4)
    t1=Newton(testfunc1,EPSILON,testfunc1.Ef,int(testfunc1.precision))
    t2=Newton(testfunc2,EPSILON,testfunc1.Ef,int(testfunc1.precision))
    t3=Newton(testfunc3,EPSILON,testfunc1.Ef,int(testfunc1.precision))
    t4=Newton(testfunc4,EPSILON,testfunc1.Ef,int(testfunc1.precision))
 
    prim1=[_ for _ in t1.integrate()]
    prim2=[_ for _ in t2.integrate()]
    prim3=[_ for _ in t3.integrate()]
    prim4=[_ for _ in t4.integrate()]
 
    plt.plot(t1.samples,prim1,label="integral "+str(t1.integral_value()))
    plt.plot(t2.samples,prim2,label="integral "+str(t2.integral_value()))
    plt.plot(t3.samples,prim3,label="integral "+str(t3.integral_value()))
    plt.plot(t4.samples,prim4,label="intrgral "+str(t4.integral_value()))
    plt.legend()

    #############
    #plt.plot(ω,σ0)
    #print(σ)
    #plt.plot(ω,σ)
    plt.show()
      

