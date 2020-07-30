"""
This module validates handles unit test cases for the Shortest Path Graph Plotter Tool
"""

import json
import os
import unittest

import flask_file
from shortestflaskplotter.shortest_path import QuickWayFinder


class TestShortPathGraphPlotter(unittest.TestCase):

    def setUp(self):
        """
        This method initializes the test case setup.

        :return: None
        """

        json_valid = {
            "node_names": {
                "1": "A",
                "2": "B",
                "3": "C"},
            "node_coordinates": {
                "A": [0, 5], "B": [1, 0], "C": [5, 1]},
            "weights_node_coordinates": [[0, 20, 0], [20, 0, 0], [0, 0, 0]],
            "node_paths": {"A": [["B", 20]], "B": [["A", 20]]}
        }

        with open('invalid.txt', 'w') as invalid_input:
            invalid_input.write('A')
        with open('router.json', 'w') as router:
            json.dump(json_valid, router)
        self.quick_way_finder = QuickWayFinder('A', 'B', 'router.json')
        self.no_path_finder = QuickWayFinder('A', 'C', 'router.json')

    def test_check_json(self):
        """
        This unit test checks the validity of the given input file.

        :return: None
        """
        self.assertEqual(flask_file.allowed_file('invalid.txt'), False)

    def test_check_traversed_path(self):
        """
        This unit test case checks the traversed path when path exists between source and target nodes.

        :return: None
        """
        self.assertEqual(self.quick_way_finder.get_the_quickest_path(), 'A -> B')

    def test_check_distance_traversed(self):
        """
        This unit test case checks the distance traversed for reaching from source to destination.

        :return: None
        """
        self.assertEqual(self.quick_way_finder.distance, 20)

    def test_path_exists_between_nodes(self):
        """
        This unit test case checks whether any path exists between source and target node.

        :return: None
        """
        self.assertEqual(self.quick_way_finder.path_exists, True)

    def test_path_not_exists_between_nodes(self):
        """
        This unit test case ensures that tool doesn't breakup when no path exists between nodes

        :return: None
        """
        self.assertEqual(self.no_path_finder.path_exists, False)

    def tearDown(self):
        """
        This method flushes out all the unwanted files once the unit test case is completed.

        :return: None
        """
        os.remove('invalid.txt')
        os.remove("router.json")


if __name__ == '__main__':
    unittest.main()
