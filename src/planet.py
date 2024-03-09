#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import Optional, List, Tuple, Dict
import queue

@unique
class Direction(IntEnum):
    """ Directions in shortcut """
    NORTH = 0
    EAST = 90
    SOUTH = 180
    WEST = 270


Weight = int
"""
Weight of a given path (received from the server)

Value:  -1 if blocked path
        >0 for all other paths
        never 0
"""


class Planet:
    """
    Contains the representation of the map and provides certain functions to manipulate or extend
    it according to the specifications
    """

    # DO NOT EDIT THE METHOD SIGNATURE
    def __init__(self):
        """ Initializes the data structure """
        self.paths = {}
        self.targets = []

    # DO NOT EDIT THE METHOD SIGNATURE
    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction],
                 weight: int):
        """
         Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it

        Example:
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
        :param start: 2-Tuple
        :param target:  2-Tuple
        :param weight: Integer
        :return: void
        """
        if start[0] not in self.paths:
            self.paths[start[0]] = {}
        if target[0] not in self.paths:
            self.paths[target[0]] = {}
        self.paths[start[0]][start[1]] = (target[0], target[1], weight)
        self.paths[target[0]][target[1]] = (start[0], start[1], weight)

    def change_weight(self, v, direction, new_weight):
        copy_target = self.paths[v][direction]
        self.add_path(start=(v, direction), target=(copy_target[0], copy_target[1]), weight=new_weight)

    # method for finding the closest vertex in Dijkstra-algorithm
    def get_closest(self, vertices, distances):
        v_min = None
        # in case we pick a path that is blocked
        for i in range(len(vertices)):
            if distances[i] != -1:
                v_min = distances[i]
        # find minimum element amongst the paths without obstacle
        for vertex in vertices:
            if distances[vertex] != -1 and distances[vertex] < distances[v_min]:
                v_min = vertex
        return v_min

    def receive_target(self, vertices, target):
        if target not in self.paths:
            self.paths[target] = {}

        self.targets.append(target)

    # DO NOT EDIT THE METHOD SIGNATURE
    def get_paths(self) -> Dict[Tuple[int, int], Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        """
        Returns all paths

        Example:
            {
                (0, 3): {
                    Direction.NORTH: ((0, 3), Direction.WEST, 1),
                    Direction.EAST: ((1, 3), Direction.WEST, 2),
                    Direction.WEST: ((0, 3), Direction.NORTH, 1)
                },
                (1, 3): {
                    Direction.WEST: ((0, 3), Direction.EAST, 2),
                    ...
                },
                ...
            }
        :return: Dict
        """

        # YOUR CODE FOLLOWS (remove pass, please!)
        return self.paths

    def add_weight(self, path: List[Tuple[int, int]]) -> None:
        pass


    def next_target(self) -> Tuple[int, int]:
        pass

    # DO NOT EDIT THE METHOD SIGNATURE
    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[List[Tuple[Tuple[int, int], Direction]]]:
        """
        Returns a shortest path between two nodes

        Examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: None, List[] or List[Tuple[Tuple[int, int], Direction]]
        """

        # YOUR CODE FOLLOWS (remove pass, please!)
        track = []
        shortest_path = {}
        vertices = set()
        for node in self.paths:
            vertices.add(Tuple[node[0], node[2]])

        while len(vertices) > 0:
            for node in vertices:
                pass

