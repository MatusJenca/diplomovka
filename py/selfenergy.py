import argparse
import json

import numpy as np

from tools.selfenergy import SelfEnergyScipy, DoubleSelfEnergyScipy

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute selfenergy")
    parser.add_argument('-t', '--taucoef', nargs='?', help='Coeficient before tau0, set to -1 for the test self energy', default=1, type=float)
    parser.add_argument('-q', '--qmax', help='q integration cutoff, (default: 10 (infinite), set to -1 to 1/(vf*tau))', default=10, type=int)
    parser.add_argument('-mn', '--min', nargs='?', help='minimum of the interval', default=0.01, type=float)
    parser.add_argument('-mx', '--max', nargs='?', help='minimum of the interval', default=1.5, type=float)
    parser.add_argument('-s', '--steps', nargs='?', help="number of linspace steps", default=100, type=int)
    parser.add_argument("--double", default=False, help="use the double lorenzian formula instead of approximation by delta function. Canceled out by '--taucoef -1', which will run the test self energy instead",
                        action="store_true")
    parser.add_argument("--dry-run", default=False, help="do not output the file",
                        action="store_true")
    parser.add_argument("-o", "--output", help="override default output file name", type=str)
    args = parser.parse_args()
    qmax = args.qmax
    suffix = 'SE_'
    # Hacky starej matere
    if args.double:
        sefunc = DoubleSelfEnergyScipy(qmax=args.qmax)
        suffix += '2L_'
    else:
        sefunc = SelfEnergyScipy(qmax=args.qmax)
    if qmax == -1:
        qmax = None
        suffix += 'Q_VF_'
    else:
        suffix += 'Q_'+str(qmax)+'_'

    erg = np.linspace(args.min, args.max, args.steps)
    if args.taucoef == -1:
        se = [[sefunc.test(e), 0] for e in erg] #error is always 0
        suffix += 'TAU_INF'
    else:
        se = [sefunc(e, taucoef=args.taucoef) for e in erg]
        suffix += 'TAU_'+str(args.taucoef)
    data = {
        'x': [e for e in erg],
        'y': [s[0] for s in se],
        'error':[s[1] for s in se]
    }
    print(data)
    if not args.dry_run:
        o = args.output
        if o is None:
            print(f"Using default output file name data/{suffix}.json")
            o = suffix
        with open("data/"+o+".json", "w") as output:
            output.write(json.dumps(data))