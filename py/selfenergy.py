import argparse
import json

import numpy as np

from tools.selfenergy import SelfEnergy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute selfenergy")
    parser.add_argument('-t', '--taucoef', nargs='?', help='Coeficient before tau0, set to -1 for the test self energy', default=1, type=float)
    parser.add_argument('-q', '--qmax', help='q integration cutoff, (default: 10 (infinite), set to -1 to 1/(vf*tau))', default=10, type=int)
    parser.add_argument('-mn', '--min', nargs='?', help='minimum of the interval', default=0.01, type=float)
    parser.add_argument('-mx', '--max', nargs='?', help='minimum of the interval', default=1.5, type=float)
    parser.add_argument('-s', '--steps', nargs='?', help="number of linspace steps", default=100, type=int)
    args = parser.parse_args()
    qmax = args.qmax
    # Hacky starej matere
    if qmax == -1:
        qmax = None
        suffix = 'Q_VF_'
    else:
        suffix = 'Q_'+str(qmax)+'_'
    sefunc = SelfEnergy(qmax=args.qmax)
    erg = np.linspace(args.min, args.max, args.steps)
    if args.taucoef == -1:
        se = [sefunc.test(e) for e in erg]
        suffix += 'TAU_INF'
    else:
        se = [sefunc(e, taucoef=args.taucoef) for e in erg]
        suffix += 'TAU_'+str(args.taucoef)
    data = {
        'x': [e for e in erg],
        'y': se
    }
    print(data)
    with open("data/"+"SE_"+suffix+".json", "w") as output:
        output.write(json.dumps(data))
