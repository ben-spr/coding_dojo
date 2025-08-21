import json
import pathlib
import unittest


def read_input_from_file(file_path: pathlib.Path):
    nodes = {}
    edges = {}
    with open(file_path, 'r') as f:
        input_dict = json.load(f)

    nodes = input_dict['Nodes']
    for key, value in input_dict['Edges'].items():
        edges[int(key)] = value
    return nodes, edges

def read_input_files():
    input_files = [f for f in pathlib.Path(pathlib.Path(__file__).parent / 'graphs').iterdir() if f.is_file()]
    return input_files

class TestSantaSolution(unittest.TestCase):

    def setUp(self):
        self.input_files = read_input_files()
        with open(pathlib.Path(pathlib.Path(__file__).parent / 'solutions/result_benjamin.json')) as f:
            self.expected_results = json.load(f)
        with open(pathlib.Path(__file__).parent / 'result.json') as f:
            self.results = json.load(f)
    
    def test_results(self):
        for input_file in self.input_files:
            filename = str(input_file).split('\\')[-1]
            with self.subTest(msg=f'Comparing solution for graph provided in {filename}'):
                graph_name = filename.replace('.json', '')
                expected_result = self.expected_results[graph_name]
                expected_gifts = expected_result['Gifts']
                expected_path = expected_result['Path']

                loaded_result = self.results.get(graph_name)
                self.assertIsNot(loaded_result, None, msg=f'SubTest failed! Tried to load results for graph {graph_name}, found none.')
                    
                gifts = loaded_result['Gifts']
                path = loaded_result['Path']

                self.assertEqual(expected_gifts, gifts, msg=f'Test failed! Expected gifts: {expected_gifts}, result found instead: {gifts}.')
                self.assertEqual(expected_path.sort(), path.sort(), msg=f'Test failed!\nExpected path: {expected_path}, sorted: {expected_path.sort()}.\n Result found instead: {path}, sorted: {path.sort()}.')


if __name__ == '__main__':
    unittest.main()
