import numpy as np
from tools.density import DensityOfStates
from tools.selfenergy import SelfEnergy
from tools.physfunction import PhysFunction
from tools.altschuler import Altschuler
from tools.derivative import derivative
import json, argparse

constants = PhysFunction()


class PrvyClen(DensityOfStates):
    def diff(self, x):
        return - self.seFunc(x)


class DruhyClen(DensityOfStates):
    def diff(self, x):
        return self.seFunc(x, taucoef=100)


def load(y, dt):
    if type(y) is str:
        return np.array([float(a) for a in dt[y]])
    else:
        return y


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", type=str, default="otazky_data")
    parser.add_argument("-f", "--file", type=str, default="rho0_test")
    parser.add_argument("-t", "--tau", type=float, default=1)
    parser.add_argument("-c", "--cfit", type=float, default=1)
    args = parser.parse_args()
    aafunc = Altschuler(taucoef=args.tau, c=args.cfit)
    sefunc = SelfEnergy(c=args.cfit, tau0=constants.base_tau0 * args.tau)
    dfunc1 = PrvyClen(sefunc)
    dfunc2 = DruhyClen(sefunc)
    with open(f"data/{args.file}.json", "r") as stream:
        data0 = json.loads(stream.read())
    erg = load('x',data0)

