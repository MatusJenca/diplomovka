import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('columns', metavar='columns', type=int, nargs=2, help="a column acumulator")
parser.add_argument('-d', '--datadir', help='the data directry (default "data" )', default='data', type=str)
parser.add_argument('-f', '--file', help='Configuration YAML file (defult: default.yaml)', nargs=1)
args = parser.parse_args()
data={
    'x':[],
    'y':[]
}
with open (f"{args.datadir}/{args.file[0]}", 'r') as stream:
    for line in stream.readlines():
        spline = [float(x.strip()) for x in line.split()]
        data['x'].append(spline[args.columns[0]])
        data['y'].append(spline[args.columns[1]])
print(json.dumps(data))




