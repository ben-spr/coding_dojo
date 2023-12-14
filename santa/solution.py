import json
import pathlib


class Solution():
    def __init__(self, nodes: list, edges: list[list], time_in_minutes: int):
        self.nodes = nodes
        self.edges = edges
        self.time = time_in_minutes

    def find_best_path(self, current_node: int = 0, minutes_left: int | None = None, path: list = [0]):
        # if seen_nodes is None:
        #     seen_nodes = [0]
        if minutes_left is None: 
            minutes_left = self.time
        # Filter for nodes that are still possible to visit
        possible_indexes = self.filter_for_possible_visits(current_node=current_node, minutes_left=minutes_left, path=path)
        # Return if no further nodes can be visited
        if not any(possible_indexes):
            return path, self.nodes[current_node]
        
        best_path = []
        gifts_max = 0
        for node in possible_indexes:
            path_temp, gifts_temp = self.find_best_path(current_node = node, minutes_left = minutes_left - self.edges[current_node][node], path = path + [node])
            if gifts_temp > gifts_max:
                best_path = path_temp
                gifts_max = gifts_temp
        return best_path, gifts_max

    
    def filter_for_possible_visits(self, current_node: int, minutes_left: int, path: list):
        # not all nodes are seen
        if not (possible_indexes := set(range(len(self.nodes))).difference(set(path))):
            return possible_indexes
        # travel time has to be shorter than time we still have
        for goal in possible_indexes.copy():
            if self.edges[current_node][goal] >= minutes_left:
                possible_indexes.remove(goal)
        # print('debug')
        return possible_indexes


def read_input_from_file(file_path: pathlib.Path):
    nodes = {}
    edges = {}
    with open(file_path, 'r') as f:
        input_dict = json.load(f)
    # for key, value in input_dict['Nodes'].items():
    #     nodes[int(key)] = value
    nodes = input_dict['Nodes']
    # print('')
    for key, value in input_dict['Edges'].items():
        edges[int(key)] = value
    return nodes, edges

def dfs_graph(nodes, edges, timeleft):
    print('')
    stack = edges[0]


def main():
    # inputfiles = [f'santa/graph_{i}.json' for i in range(1,11)]
    inputfiles = [f for f in pathlib.Path(pathlib.Path(__file__).parent / 'graphs').iterdir() if f.is_file()]
    # for i in range(1):
    for i in range(len(inputfiles)):
        nodes, edges = read_input_from_file(inputfiles[i])
        solution = Solution(nodes=nodes, edges=edges, time_in_minutes=4*60)
        path, gifts = solution.find_best_path()
        # with open(inputfiles[i], 'r') as f:
        #     # input_str = f.read()
        #     test = json.load(f)
        print(f'{inputfiles[i]}: the optimal path for Santa results in {gifts} gifts being delivered and is: {path}.')

if __name__ == '__main__':
    main()
