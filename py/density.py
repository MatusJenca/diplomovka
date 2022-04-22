import numpy as np
from tools.density import DensityOfStates
from tools.selfenergy import SelfEnergy
import argparse, json
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-mn', '--min', nargs='?', help='minimum of the interval', default=0.95, type=float)
    parser.add_argument('-mx', '--max', nargs='?', help='minimum of the interval', default=1.05, type=float)
    parser.add_argument('-s', '--steps', nargs='?', help="number of linspace steps", default=100, type=int)
    parser.add_argument('-t', '--taumultiplier', help='base tau0 multiplyier ', default=1, type=float)
    args = parser.parse_args()

    suffix = str(args.taumultiplier)
    sefunc = SelfEnergy()
    sefunc.tau0 = sefunc.base_tau0*args.taumultiplier
    print(sefunc.tau0)
    dfunc = DensityOfStates(sefunc)
    erg = np.linspace(args.min, args.max, args.steps)
    dens = [dfunc(e) for e in erg]
    data = {
        'x': [e for e in erg],
        'y': dens
    }
    print(data)
    with open("data/"+"DOS_TAU_"+suffix+".json", "w") as output:
        output.write(json.dumps(data))
