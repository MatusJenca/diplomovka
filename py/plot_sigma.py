import sys
sys.path.append('tools')
import numpy as np
import matplotlib.pyplot as plt
from sigma import Sigma,TestF
from integrator import Newton,EPSILON
if __name__=="__main__": 

    sigmafunc_nocorr=Sigma(τ=6.58e-16,corr=False)
    sigmafunc_corr=Sigma(τ=6.58e-16,corr=True)
    ω=(np.linspace(EPSILON,1,1000)*sigmafunc_nocorr.Ef)/sigmafunc_nocorr.h
    σ0=sigmafunc_nocorr(ω)
    σ=sigmafunc_corr(ω)
    plt.plot(ω,σ0,label="bez korekcie")
    plt.plot(ω,σ,label="s korekciou")
    plt.xlabel(r"$\omega$")
    plt.ylabel(r"$\sigma$")
    plt.legend()

    #############
    #plt.plot(ω,σ0)
    #print(σ)
    #plt.plot(ω,σ)
    plt.show()
      

