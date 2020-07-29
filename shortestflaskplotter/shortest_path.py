"""
This modules manages the business logic of the service. It processes the JSON files and gives the shortest path from one node to the other./
"""
import json
from functools import reduce

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('agg')


class QuickWayFinder(object):
    """
    This class handles data processing and output file generation
    """

    def __init__(self, node1, node2, json_file_name):
        self.node1 = node1
        self.node2 = node2
        self.node_coordinates = None
        self.node_names = None
        self.json_file_name = json_file_name
        self.weights_node_coordinates = None
        self.node_paths = None
        self.traversed_path = None
        self.distance = None
        self.plt = None
        self.process_json()
        self.prepare_coordinates()
        self.highlight_the_shortest_path()

    def process_json(self):
        """
        This method cleanses the JSON file.

        :return: None
        """
        with open(self.json_file_name) as json_file:
            data = json.load(json_file)
            self.node_coordinates = data["node_coordinates"]
            self.node_names = data["node_names"]
            self.weights_node_coordinates = data["weights_node_coordinates"]
            self.node_paths = data["node_paths"]

    def prepare_coordinates(self):
        """
        This method initializes the graphs based on the coordinates from the JSON file.

        :return: None
        """
        xCoord = [int(self.node_coordinates[k][0]) for k in sorted(self.node_coordinates)]
        yCoord = [int(self.node_coordinates[k][1]) for k in sorted(self.node_coordinates)]
        plt.plot(xCoord, yCoord, 'bo')
        plt.axis([-1, 7, -1, 9])
        for i in range(len(self.node_names)):
            plt.text(xCoord[i] - 0.5, yCoord[i], self.node_names[str(i + 1)])
        for i in range(len(self.node_names)):
            for j in range(len(self.node_names)):
                if self.weights_node_coordinates[i][j]:
                    plt.plot([xCoord[i], xCoord[j]], [yCoord[i], yCoord[j]], 'b')

    def get_the_quickest_path(self):
        """
        This method initiates the logic for the shortest path between the two nodes.

        :return: Traversed Edges and Nodes
        """
        traversed_path, distance = self.find_shortest_path(self.node_paths, self.node1, self.node2)
        self.traversed_path = traversed_path
        self.distance = distance
        print(f"The traversed path is {traversed_path}")
        print(f"The total weight along the traversed path {distance}")
        return traversed_path

    def highlight_the_shortest_path(self):
        """
        This module highlights the shortest path with red color.

        :return: None
        """
        traversed_path = self.get_the_quickest_path()
        # Drawing of coordinates
        mydrawing = traversed_path.split('-> ')
        print([int(self.node_coordinates[n.rstrip()][0]) for n in mydrawing])
        plt.plot([int(self.node_coordinates[n.rstrip()][0]) for n in mydrawing],
                 [int(self.node_coordinates[n.rstrip()][1]) for n in mydrawing], color="red")
        self.plt = plt

    def find_shortest_path(self, graph, start, target):
        """
        This module handles the logic for the shortest path finding between two nodes.

        :param graph: Graph Structure
        :param start: Source Node
        :param target: Destination Node
        :return: traversed node and distance calculated.
        """
        inf = reduce(lambda x, y: x + y, (i[1] for u in graph for i in graph[u]))
        dist = dict.fromkeys(graph, inf)
        prev = dict.fromkeys(graph)
        q = list(graph.keys())
        dist[start] = 0
        while q:
            u = min(q, key=lambda x: dist[x])
            q.remove(u)
            for v, w in graph[u]:
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u

        trav = []
        temp = target
        while temp != start:
            trav.append(prev[temp])
            temp = prev[temp]
        trav.reverse()
        trav.append(target)
        return " -> ".join(trav), dist[target]
