import sys
sys.path.append('tools')
import numpy as np
import matplotlib.pyplot as plt
from sigma import Sigma,TestF
from integrator import Newton,EPSILON
if __name__=="__main__": 

    sigmafunc=Sigma(τ=6.58e-16)
    omgcoef=(sigmafunc.Ef)/sigmafunc.h
    ω=np.linspace(0.5,2,1000)*omgcoef
    σ=sigmafunc(ω)
    F=sigmafunc.F(ω)
    plt.plot(ω,σ,label="bez korekcie")
    plt.plot(ω,σ*F,label="s korekciou")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\sigma$")
    plt.legend()
    plt.show()
    #############
    #plt.plot(ω,σ0)
    #print(σ)
    #plt.plot(ω,σ)
    #plt.savefig("sigma.png")
    plt.clf()
    plt.plot(ω,F,label="funkcia F")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$F$")
    plt.legend()
    plt.show()
    #plt.savefig("F.png")    

