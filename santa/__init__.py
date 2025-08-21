import pathlib

import santa.graphs.graph_generator as graph_generator
import solutions.solution_benjamin

def fresh_setup():
    folder = pathlib.Path(__file__).parent.resolve()
    graph_generator.main()
    solutions.solution_benjamin.main()
