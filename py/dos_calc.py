import argparse
import json
import sys

import numpy as np
from tools.selfenergy import SelfEnergy, SelfEnergyScipy, DoubleSelfEnergy, DoubleSelfEnergyScipy
from tools.density import DensityOfStates, DensityOfStatesScipy


# Evil Yanderedev be like
def output_name(args):
    name = '_'.join([
        {
            'selfenergy': 'SE',
            'density': 'DOS'
        }[args.calculation],
        {
            'square': '1LS',
            'ssquare': '2LS',
            'quad': '1LQ',
            'dquad': '2LQ'
        }[args.int_method]
    ])
    if args.calculation == 'selfenergy':
        name += f'_Q_{args.qmax}'
    name += f'_TAU_{args.taucoef}'
    return name


def calc_selfenergy(args):
    erg = np.linspace(args.min, args.max, args.steps)
    try:
        sefunc = {
            'square': SelfEnergy(qmax=args.qmax),
            'dsquare': DoubleSelfEnergy(qmax=args.qmax),
            'quad': SelfEnergyScipy(qmax=args.qmax),
            'dquad': DoubleSelfEnergyScipy(qmax=args.qmax),
        }[args.int_method]
    except KeyError:
        print(f"invalid integration method {args.int_method}, type dos_calc -h for help")
        return
    if args.taucoef == -1:
        se = [[sefunc.test(e), 0] for e in erg]  # error is always 0
    else:
        if args.int_method in ('square', 'dsquare'):
            se = [[sefunc(e, taucoef=args.taucoef), 0] for e in erg]
        else:
            se = [sefunc(e, taucoef=args.taucoef) for e in erg]
    return {
        'x': [e for e in erg],
        'y': [s[0] for s in se],
        'error': [s[1] for s in se]
    }


def calc_dos(args):
    erg = np.linspace(args.min, args.max, args.steps)
    try:
        dfunc = {
            'square': DensityOfStates(SelfEnergy()),
            'dsquare': DensityOfStates(DoubleSelfEnergy()),
            'quad': DensityOfStatesScipy(SelfEnergyScipy()),
            'dquad': DensityOfStatesScipy(DoubleSelfEnergyScipy()),
        }[args.int_method]
    except KeyError:
        print(f"invalid integration method {args.int_method}, type dos_calc -h for help")
        return
    dfunc.seFunc.tau0 = dfunc.seFunc.base_tau0 * args.taucoef
    dens = [dfunc(e) for e in erg]

    return {
        'x': [e for e in erg],
        'y': [d[0] for d in dens],
        'errors': [d[1] for d in dens]
    }


if __name__ == "__main__":
    # Arg Parse

    # Global
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="calculation")
    parser.add_argument("--dry-run", default=False, help="do not output the file", action="store_true")
    parser.add_argument("-o", "--output", help="override default output file name", type=str)
    parser.add_argument("-im", "--int-method", default="square", type=str,
                        help=
                        '''
                        an integration method used to calculate the value.
                        Valid options:
                            square (default): integrate over small squares 1D    
                            dsquare: integrate over small squares 2D (WARNING: SLOW)
                            quad: integrate using scipy.integrate.quad   
                            dquad: integrate using scipy.integrate.quad  
                        '''
                        )
    # Self Energy
    se_parser = subparser.add_parser('selfenergy')
    se_parser.add_argument('-t', '--taucoef', nargs='?',
                           help='Coeficient before tau0, set to -1 for the test self energy',
                           default=1, type=float)
    se_parser.add_argument('-q', '--qmax',
                           help='q integration cutoff, (default: 10 (infinite), set to -1 to 1/(vf*tau))',
                           default=10, type=int)
    se_parser.add_argument('-mn', '--min', nargs='?', help='minimum of the interval', default=0.01, type=float)
    se_parser.add_argument('-mx', '--max', nargs='?', help='minimum of the interval', default=1.5, type=float)
    se_parser.add_argument('-s', '--steps', nargs='?', help="number of linspace steps", default=100, type=int)
    # Density of states
    dos_parser = subparser.add_parser('density')
    dos_parser.add_argument('-mn', '--min', nargs='?', help='minimum of the interval', default=0.95, type=float)
    dos_parser.add_argument('-mx', '--max', nargs='?', help='minimum of the interval', default=1.05, type=float)
    dos_parser.add_argument('-s', '--steps', nargs='?', help="number of linspace steps", default=100, type=int)
    dos_parser.add_argument('-t', '--taucoef', help='base tau0 multiplier ', default=1, type=float)
    args = parser.parse_args()
    try:
        data = {
            'selfenergy': calc_selfenergy,
            'density': calc_dos,
        }[args.calculation](args)
    except KeyError:
        parser.print_usage()
        sys.exit()
    print(data)
    if not args.dry_run:
        o = args.output
        if o is None:
            o = output_name(args)
        oname = 'data/' + o + '.json'
        print(f'using output name {oname}')
        with open(oname, 'w') as stream:
            stream.write(json.dumps(data))
