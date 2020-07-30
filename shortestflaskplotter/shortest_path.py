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
        self.path_exists = False
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
        xCoord = [self.node_coordinates[k][0] for k in sorted(self.node_coordinates)]
        yCoord = [self.node_coordinates[k][1] for k in sorted(self.node_coordinates)]
        plt.plot(xCoord, yCoord, 'bo')
        x_max, x_min, y_max, y_min = self.get_plotter_coordinates()
        plt.axis([x_max, x_min, y_max, y_min])
        plt.xlabel('X Coordinate of Node', fontsize=16)
        plt.ylabel('Y Coordinate of Node', fontsize=16)
        for i in range(len(self.node_names)):
            plt.text(xCoord[i] - 0.1, yCoord[i] - 0.1, self.node_names[str(i + 1)])
        for i in range(len(self.node_names)):
            for j in range(len(self.node_names)):
                if self.weights_node_coordinates[i][j]:
                    plt.annotate(f'{self.weights_node_coordinates[i][j]}\n',
                                 xy=((xCoord[i] + xCoord[j]) / 2, (yCoord[i] + yCoord[j]) / 2),
                                 fontsize="medium")
                    plt.plot([xCoord[i], xCoord[j]], [yCoord[i], yCoord[j]], color='blue')

    def get_plotter_coordinates(self):
        """
        This method finds the max and min X and Y coordinates.

        :return: x and y min,max coordinates
        """
        x_max = 0
        y_max = 0
        x_min = 0
        y_min = 0
        nodes_coords = self.node_coordinates.values()
        for coord in nodes_coords:
            if coord[0] > x_max:
                x_max = coord[0]
            if coord[0] < x_min:
                x_min = coord[0]
            if coord[1] > y_max:
                y_max = coord[1]
            if coord[1] < y_min:
                y_min = coord[1]
        return x_max, x_min, y_max, y_min

    def get_the_quickest_path(self):
        """
        This method initiates the logic for the shortest path between the two nodes.

        :return: Traversed Edges and Nodes
        """
        traversed_path, distance = self.find_shortest_path(self.node_paths, self.node1, self.node2)
        self.traversed_path = traversed_path
        self.distance = distance
        return traversed_path

    def highlight_the_shortest_path(self):
        """
        This module highlights the shortest path with red color.

        :return: None
        """
        traversed_path = self.get_the_quickest_path()
        if traversed_path:
            self.path_exists = True
        else:
            return
        # Drawing of coordinates
        mydrawing = traversed_path.split('-> ')
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
        if target not in prev:
            return None, None
        trav = []
        temp = target
        while temp != start and target:
            trav.append(prev[temp])
            temp = prev[temp]
        trav.reverse()
        trav.append(target)
        return " -> ".join(trav), dist[target]
