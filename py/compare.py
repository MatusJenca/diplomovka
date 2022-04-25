import numpy as np
import json
import argparse


def lst(f1, f2):
    print(100 * "_" + "\n")
    print(f"{f1[0]} x\t{f1[0]} \t y{f2[0]} x\t{f2[0]} y")
    print(100 * "_")
    for i in range(len(f1[1]['x'])):
        print(f"{f1[1]['x'][i]}\t{f1[1]['y'][i]}\t{f2[1]['x'][i]}\t{f2[1]['y'][i]}\t")
    print(100 * "_")


def diff(f1, f2):
    print(f"Differnce values for {f1[0]} and {f2[0]}")
    print(100 * "_")
    diffs = []
    for i in range(len(f1[1]['x'])):
        if np.abs(f1[1]['x'][i] - f2[1]['x'][i]) > 1e-4:
            print(f"Warning: different x values {f1[0]} = {f1[1]['x'][i]} and {f2[0]} = {f1[1]['x'][i]}")
        d = f1[1]['y'][i] - f2[1]['y'][i]
        diffs.append(d)
        print(f"\t{d}")
    print(f"Average:{np.average(np.array(diffs))}")


def ratio(f1, f2):
    print(f"Ratio values for {f1[0]} and {f2[0]}")
    print(100 * "_")
    ratios = []
    for i in range(len(f1[1]['x'])):
        if np.abs(f1[1]['x'][i] - f2[1]['x'][i]) > 1e-4:
            print(f"Warning: different x values {f1[0]} = {f1[1]['x'][i]} and {f2[0]} = {f1[1]['x'][i]}")
        r = f1[1]['y'][i] / f2[1]['y'][i]
        ratios.append(r)
        print(f"\t{r}")
    print(f"Average:{np.average(np.array(ratios))}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='file', type=str, nargs=2, help="a file acumulator")
    parser.add_argument('-m', '--method', default='list', type=str, help=
    '''
        a comparing method valid values:
            list
            diff
            ratio
        defult: list
    ''')
    args = parser.parse_args()
    d1, d2 = [(f, json.loads(open('data/' + f.upper() + '.json', 'r').read())) for f in args.files]
    {
        'list': lst,
        'diff': diff,
        'ratio': ratio
    }[args.method](d1, d2)
