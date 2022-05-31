import numpy as np
import matplotlib.pyplot as plt
import json
import argparse


def nf(x):
    if x == '':
        return None
    return float(x)


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', default='otazky_data', type=str)
parser.add_argument('-l', '--limit_x', default=0.01, type=nf)
parser.add_argument('-ym', '--ylim-btm', default=-1, type=nf)
parser.add_argument('-yx', '--ylim-top', default=0.75, type=nf)
args = parser.parse_args()
with open(f"data/{args.file}.json", "r") as stream:
    data = json.loads(stream.read())



def load(y, dt=data):
    if type(y) is str:
        return np.array([float(a) for a in dt[y]])
    else:
        return y


def join(a, b, dt=data):
    aa = load(a, dt)
    bb = load(b, dt)
    ret = np.where(aa < bb, aa, bb)
    print(ret)
    return ret


def plus(a, b, dt=data):
    aa = load(a, dt)
    bb = load(b, dt)
    return aa + bb


erg = load('energy')
rho0 = load('rho0')

rho_ast = 7.24415793714746e+46
otazka1 = (
        (rho0 - rho_ast)
        /
        rho_ast
)
otazka2 = plus(join('altschuler', 'prvy_clen'), 'druhy_clen')

plt.xlim(left=1 - args.limit_x, right=1 + args.limit_x)
plt.ylim(top=args.ylim_top, bottom=args.ylim_btm)

plt.plot(erg, otazka1)
plt.xlabel(r'$\mathcal{E}/\mathcal{E}_{F}$')
plt.ylabel(r'$(\rho_0(\mathcal{E})-\rho_0(\mathcal{E}_*))/\rho_0(\mathcal{E}_*)$')
plt.show()
