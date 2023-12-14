import json
import pathlib
import random

FILE_DIRECTORY = pathlib.Path(__file__).parent.resolve()


def generate_random_graph(num_nodes: int|None = None):
    if num_nodes is None or num_nodes < 2:
        # Generate a random number of nodes between 10 and 200
        num_nodes = random.randint(10, 200)

    # Create nodes with random integer values
    nodes = {i: random.randint(1, 20) for i in range(num_nodes)}

    # Ensure that the 0th node has the value 0
    nodes[0] = 0

    # Create edges connecting all nodes to all other nodes
    # edges = [(i, j) for i in range(num_nodes) for j in range(i + 1, num_nodes)]
    edges = {i: [0 for _ in range(num_nodes)] for i in range(num_nodes)}
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            #  edges[i].append(round(random.uniform(0.1, 10.0), 1))
             edges[i][j] = round(random.uniform(0.1, 120.0), 1)
             edges[j][i] = edges[i][j]
    # edges = [(i, j, round(random.uniform(0.1, 10.0), 1)) for i in range(num_nodes) for j in range(i + 1, num_nodes)]

    return num_nodes, nodes, edges


def write_graph_to_json(file_name: str, node_values: dict, edge_list: list):
    graph_dict = {
        'Nodes': node_values,
        'Edges': edge_list
    }
    graph_json_object = json.dumps(graph_dict)
    file_path = pathlib.Path(FILE_DIRECTORY / 'graphs' / f'{file_name}.json')
    # file_path = pathlib.Path(FILE_DIRECTORY / f'{file_name}.json')
    # with open(f'{FILE_DIRECTORY}\\{file_name}.json', 'w') as f:
    with open(file_path, 'w') as f:
            f.write(graph_json_object)


def main():
    for i in range(10):
        num_nodes = random.randint(10, 20)
        num_nodes, node_values, edge_list = generate_random_graph(num_nodes=num_nodes)
        write_graph_to_json(f'graph_{i+1}', node_values, edge_list)
        # write_string = f'Nodes: {node_values},\nEdges: {edge_list}'
        # with open(f'graph_{i+1}.txt', 'w') as f:
        #     f.write(write_string)


if __name__ == '__main__':
    main()
