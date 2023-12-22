import json
from multiprocessing import Pool
from multiprocessing import Process
import pathlib


class Solution():
    def __init__(self, nodes: list, edges: list[list], time_in_minutes: int, debug: bool = False):
        self.nodes = nodes
        self.edges = edges
        self.time = time_in_minutes
        self.debug = debug

    def find_best_path(self, current_node: int = 0, path: list = [0]):
        # print(f'Current node: {current_node}')
        minutes_left = self.calculate_travel_time_left(path)
        # print(f'Minutes left: {minutes_left}')
        
        # Filter for nodes that are still possible to visit
        possible_indexes = self.filter_for_possible_visits(current_node=current_node, minutes_left=minutes_left, path=path)
        # print(f'Possible nodes: {possible_indexes}')
        
        # Return if no further nodes can be visited
        if not any(possible_indexes):
            return path, self.nodes[current_node]
        
        best_path = path
        gifts_max = self.calculate_gifts_collected(path)
        for node in possible_indexes:
            path_temp, gifts_temp = self.find_best_path(current_node = node, path = path + [node])
            if gifts_temp > gifts_max:
                best_path = path_temp
                gifts_max = gifts_temp
        return best_path, gifts_max

    def calculate_gifts_collected(self, path: list):
        gifts = 0
        for node in path:
            gifts += self.nodes[node]
        return gifts

    def calculate_travel_time_left(self, path):
        time_left = self.time
        if len(path) == 1:
            return time_left
        
        previous_node = path[0]
        for node in path[1:]:
            time_left -= self.edges[previous_node][node]
            previous_node = node
        return time_left
    
    def filter_for_possible_visits(self, current_node: int, minutes_left: int, path: list):
        # not all nodes are seen
        if not (possible_indexes := set(range(len(self.nodes))).difference(set(path))):
            return possible_indexes
        # travel time has to be shorter than time we still have
        for goal in possible_indexes.copy():
            if self.edges[current_node][goal] >= minutes_left:
                possible_indexes.remove(goal)
        return possible_indexes


def read_input_from_file(file_path: pathlib.Path):
    nodes = {}
    edges = {}
    with open(file_path, 'r') as f:
        input_dict = json.load(f)

    nodes = input_dict['Nodes']
    for key, value in input_dict['Edges'].items():
        edges[int(key)] = value
    return nodes, edges

def solve_and_print_results(i: int, solution: Solution):
        inputfiles = read_input_files()
        path, gifts = solution.find_best_path()
        graph_name = str(inputfiles[i]).split('\\')[-1].replace('.json', '').replace('_', ' ').title()
        print(f'{graph_name}: the optimal path for Santa results in {gifts} gifts being delivered and is: {path}.')

def solve_and_write_results_to_json(i: int, solution: Solution):
        inputfiles = read_input_files()
        folder = pathlib.Path(__file__).parent.resolve()
        filename = 'result_benjamin.json'
        savepath = pathlib.Path(folder / filename)
        graph_name = str(inputfiles[i]).split('\\')[-1].replace('.json', '')
        if savepath.is_file():
            print(f'Save file {str(savepath)} exists. Trying to load results.')
            with open(savepath, 'r') as f:
                results = json.load(f)
        else:
            results = dict()
        
        path, gifts = solution.find_best_path()

        results[graph_name] = {
            'Gifts': gifts,
            'Path': path
        }
        with open(savepath, 'w') as f:
            results_json_object = json.dumps(results)
            f.write(results_json_object)
        print(f'{graph_name}: the optimal path for Santa results in {gifts} gifts being delivered and is: {path}.')

def read_input_files():
    input_files = [f for f in pathlib.Path(pathlib.Path(__file__).parent.parent / 'graphs').iterdir() if f.is_file()]
    return input_files

def multithreaded_solution(debug: bool = False):
    inputfiles = read_input_files()
    solution_objects = []
    # processes = []
    max_index = 1 if debug else len(inputfiles)
    
    for i in range(max_index):
        nodes, edges = read_input_from_file(inputfiles[i])
        solution_objects.append(Solution(nodes=nodes, edges=edges, time_in_minutes=4*60))

    p = Pool(processes=len(inputfiles))
    results = p.map(Solution.find_best_path, solution_objects)
    p.close()


    folder = pathlib.Path(__file__).parent.resolve()
    solution_filename = 'result_benjamin.json'
    savepath = pathlib.Path(folder / solution_filename)
    result_dict = dict()
    for i, (path, gifts) in enumerate(results):
        graph_name = str(inputfiles[i]).split('\\')[-1].replace('.json', '')
        result_dict[graph_name] = {
            'Gifts': gifts,
            'Path': path
        }
    
    with open(savepath, 'w') as f:
            results_json_object = json.dumps(result_dict)
            f.write(results_json_object)


def singlethreaded_solution(debug: bool = False):
    inputfiles = read_input_files()
    max_index = 1 if debug else len(inputfiles)
    for i in range(max_index):
        nodes, edges = read_input_from_file(inputfiles[i])
        solution = Solution(nodes=nodes, edges=edges, time_in_minutes=4*60)
        gifts, path = solution.find_best_path()
        graph_name = str(inputfiles[i]).split('\\')[-1].replace('.json', '').replace('_', ' ').title()
        print(f'{graph_name}: the optimal path for Santa results in {gifts} gifts being delivered and is: {path}.')

def main():
    # singlethreaded_solution(debug = False)
    multithreaded_solution(debug = False)
    


if __name__ == '__main__':
    main()
