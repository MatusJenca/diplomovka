import numpy as np
from tools.density import DensityOfStates
from tools.selfenergy import SelfEnergy
from tools.physfunction import PhysFunction
from tools.altschuler import Altschuler
import json,argparse

constants = PhysFunction()

class PrvyClen(DensityOfStates):
    def diff(self, x):
        return - self.seFunc(x)


class DruhyClen(DensityOfStates):
    def diff(self, x):
        return self.seFunc(x, taucoef=100)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output",type=str,default="final_data")
    parser.add_argument("-t", "--tau", type=float, default=1)
    parser.add_argument("-c", "--cfit", type=float, default=1)
    parser.add_argument('-mn', '--min', nargs='?', help='minimum of the interval', default=0.95, type=float)
    parser.add_argument('-mx', '--max', nargs='?', help='minimum of the interval', default=1.05, type=float)
    parser.add_argument('-s', '--steps', nargs='?', help="number of linspace steps", default=100, type=int)
    args = parser.parse_args()
    aafunc = Altschuler(taucoef=args.tau, c=args.cfit)
    sefunc = SelfEnergy(c=args.cfit, tau0=constants.base_tau0*args.tau)
    dfunc1 = PrvyClen(sefunc)
    dfunc2 = DruhyClen(sefunc)
    erg = np.linspace(args.min, args.max, args.steps)
    data = {
        'energy': [e for e in erg],
        'altschuler': [aafunc(e) for e in erg],
        'prvy_clen': [dfunc1(e)[0] for e in erg],
        'druhy_clen': [dfunc2(e)[0]for e in erg],
    }
    with open(f"data/{args.output}.json", "w") as stream:
        stream.write(json.dumps(data))
