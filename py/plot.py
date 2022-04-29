import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import json, argparse, yaml


def fill_path(f, directory, ext):
    if not f[:len(directory)] == directory:
        f = directory + "/" + f
    if not f[-(len(ext)):] == ext:
        f += ext
    return f.strip()


def remove_path(f, directory, ext):
    if f[:len(directory)] == directory:
        f = f[len(directory) + 1:]
    if f[-len(ext):] == ext:
        f = f[:-len(ext)]
    return f.strip()


if __name__ == "__main__":
    with open("config/default.yaml", 'r') as stream:
        default_cfg = yaml.safe_load(stream)
    parser = argparse.ArgumentParser(description="Plot given file (s)")
    parser.add_argument('files', metavar='file', type=str, nargs='+', help="a file acumulator")
    parser.add_argument('-d', '--datadir', help='the data directry (default "data" )', default='data', type=str)
    parser.add_argument('-o', '--output', help='output file (default: show the figure instead)')
    parser.add_argument('-c', '--config', help='Configuration YAML file (defult: default.yaml)')
    parser.add_argument('-m','--metadata', help='display metadata over the plot')
    args = parser.parse_args()
    if args.config is not None:
        with open(fill_path(args.config, 'config', '.yaml')) as stream:
            config = yaml.safe_load(stream)
    else:
        config = default_cfg


    def load_value(value):
        if value in config:
            return config[value]
        return default_cfg[value]


    for i, file in enumerate(args.files):
        file = file.upper()
        file = fill_path(file, args.datadir, '.json')
        name = remove_path(file, args.datadir, '.json').lower()

        with open(file) as stream:
            data = json.loads(stream.read())
            xaxis = np.array(data['x'])
            yaxis = np.array(data['y'])
            if name in config:
                plot_cfg = config[name]
            else:
                plot_cfg = default_cfg['plot']


            def load_subvalue(value):
                # Dalsie heky starej matere
                if value in plot_cfg:
                    return plot_cfg[value]
                if 'plot' in config:
                    if value in config['plot']:
                        return config['plot'][value]
                return default_cfg['plot'][value]


            plt.plot(xaxis, yaxis,
                     linewidth=load_subvalue('width'),
                     label=load_subvalue('label'),
                     color=load_subvalue('color')
                     )
    if load_value('legend'):
        plt.legend()
    plt.xlabel(load_value('xaxis'))
    plt.ylabel(load_value('yaxis'))
    plt.title(load_value('title'))
    if args.output is None:
        plt.show()
    else:
        plt.savefig(fill_path(args.output, 'img', '.pdf'))
