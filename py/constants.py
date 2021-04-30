import numpy as np
'''
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
#tienenie
ks=kf
#fermiho energiay
Ef=(h**2*kf**2)/(2*m)
print(Ef)
#fermiho rychlost
vf=np.sqrt((2*Ef)/(m))
#tau0
τ0=5*6.58e-16
#permitivita
ε0=8.854187e-12

