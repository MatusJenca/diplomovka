import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import json
import argparse


def nf(x):
    if x == '':
        return None
    return float(x)


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', default='final_data', type=str)
parser.add_argument('-ym', '--ylim-btm', default=-1.5e-5, type=nf)
parser.add_argument('-yx', '--ylim-top', default=1.5e-5, type=nf)
args = parser.parse_args()
with open(f"data/{args.file}.json", "r") as stream:
    data = json.loads(stream.read())


def load(y, dt=data):
    if type(y) is str:
        return np.array([float(a) for a in dt[y]])
    else:
        return y


def pt(y, aax, dt=data, **kwargs):
    aax.plot(load('energy'), load(y), **kwargs)


def new():
    plt.clf()
    plt.axhline(y=0, color='black', linestyle="--", linewidth=1)
    plt.ylim(top=1e-5, bottom=-1.5e-5)


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


axlabels = [
    ['a', 'b'],
    ['c', 'd']
    #['e', 'f']
]
figure, axis = plt.subplots(2, 2, figsize=(7, 7))
figure.tight_layout()
for i, ax in enumerate(axis):
    for j, a in enumerate(ax):
        a.axis(ymax=args.ylim_top, ymin=args.ylim_btm)
        a.axhline(y=0, color='black', linestyle="--", linewidth=1)

        if i == 1:
            a.set_xlabel(r'$\mathcal{E}/\mathcal{E}_{F}$')
        if j == 0:
            a.set_ylabel(r'$(\rho(\mathcal{E})-\rho_0(\mathcal{E}))/\rho_0(\mathcal{E})$')
        a.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
        a.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        a.set_title(f"{axlabels[i][j]})", y=1.0, pad=-14, loc='left', x=0.1)
pt('prvy_clen', axis[0, 0])
pt('altschuler', axis[0, 0], color='red')
pt('druhy_clen', axis[0, 1])
pt(join('altschuler', 'prvy_clen'), axis[1, 0])
pt(plus(join('altschuler', 'prvy_clen'), 'druhy_clen'), axis[1, 1])
#pt(join('altschuler', 0), axis[2, 0])
#pt(plus(join('altschuler', 0), 'druhy_clen'), axis[2, 1])
plt.subplots_adjust(left=0.1, bottom=0.1)
#
#plt.show()
plt.savefig(f'../img/{args.file}.pdf')
