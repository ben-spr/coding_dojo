import json
import pathlib


def read_input_from_file(file_path: pathlib.Path):
    nodes = {}
    edges = {}
    with open(file_path, 'r') as f:
        input_dict = json.load(f)
    for key, value in input_dict['Nodes'].items():
        nodes[int(key)] = value
    print('')
    for key, value in input_dict['Edges'].items():
        edges[int(key)] = value
    return nodes, edges

def dfs_graph(nodes, edges):
    print('')
    stack = edges[0]


def main():
    # inputfiles = [f'santa/graph_{i}.json' for i in range(1,11)]
    inputfiles = [f for f in pathlib.Path(pathlib.Path(__file__).parent / 'graphs').iterdir() if f.is_file()]
    for i in range(1):
        nodes, edges = read_input_from_file(inputfiles[i])
        dfs_graph(nodes, edges)
        # with open(inputfiles[i], 'r') as f:
        #     # input_str = f.read()
        #     test = json.load(f)
    print('debug')

if __name__ == '__main__':
    main()
