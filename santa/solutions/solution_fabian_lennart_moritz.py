from dataclasses import dataclass
import json
from typing import NamedTuple
 
 
class Result(NamedTuple):
    Gifts: int
    Path: list[int]
 
    def to_json(self):
        ...
 
 
 
@dataclass
class Graph:
    nodes: list[int]
    edges: list[list[int]]
 
 
def load_graph(path):
    with open(path, 'r', encoding="utf-8") as infile:
        graph = json.load(infile)
    nodes = graph["Nodes"]
    edges = graph["Edges"]
    edges = [edges[str(num)] for num in range(len(nodes))]
    return Graph(nodes, edges)
 
 
def solve_problem(graph: Graph):
    time_remaining = 240.0
 
    known_states = {}
 
    def traverse(current_idx, time_remaining, visited=None) -> int:
        if time_remaining <= 0.0:
            return 0, []
       
        if not visited:
            visited = []
       
        presents = graph.nodes[current_idx] if current_idx not in visited else 0
        max_ = 0
        best_path = []
        for node_idx in [n for n in range(len(graph.nodes)) if not n == current_idx]:
            next_val, path = traverse(node_idx, time_remaining - graph.edges[current_idx][node_idx], visited=visited + [current_idx])
            if next_val >= max_:
                max_ = next_val
                best_path = path
        return presents + max_, best_path + [current_idx]
    return traverse(0, time_remaining)
 
 
 
   
 
 
solutions = []
for num in range(1, 21):
    solutions.append(solve_problem(load_graph(f"graphs/graph_{num:02}.json")))