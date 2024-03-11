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
        self.position = []
        self.prev_position = []

    def change_position(self, x, y):
        if len(self.position) == 2:
            self.prev_position = self.prev_position
        self.position = [x, y]

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

    def intelligent_search(self):
        pass

    @staticmethod
    def get_closest_vertex(vertices, distances):
        v_min = vertices.pop()
        vertices.add(v_min)

        # find minimum element amongst the paths without obstacle
        for vertex in vertices:
            if distances[vertex] < distances[v_min]:
                v_min = vertex
        return v_min

    def get_neighbours(self, vertex, vertices):
        neighbours = []
        for direction in self.paths[vertex]:
            if self.paths[vertex][direction][0] not in vertices:
                continue
            distance = float('inf')
            if self.paths[vertex][direction][2] != -1:
                distance = self.paths[vertex][direction][2]
            neighbour = (self.paths[vertex][direction][0], distance)
            neighbours.append(neighbour)
        return neighbours

    def receive_target(self, vertices, target):
        if target not in self.paths:
            self.paths[target] = {}

        self.targets.append(target)


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
        if target not in self.paths or self.paths[target] == {}:
            return None
        track = []
        prev_node = {}
        vertices = set()
        c_paths = list(self.paths.keys())
        for i in range(len(self.paths)):
            vertices.add(c_paths[i])
        distances = {v: float('inf') for v in vertices}
        distances[start] = 0
        while len(vertices) > 0:
            v = self.get_closest_vertex(vertices, distances)
            if distances[v] == float('inf'):
                return None
            elif v == target:
                break
            vertices.remove(v)
            for w in self.get_neighbours(v, vertices):
                new_distance = distances[v] + w[1]
                if new_distance < distances[w[0]]:
                    distances[w[0]] = new_distance
                    prev_node[w[0]] = v
        # backtracking
        current_node = target
        while current_node != start:
            for direction in self.paths[current_node]:
                if self.paths[current_node][direction][0] == prev_node[current_node]:
                    track.append((current_node, self.paths[current_node][direction][1], distances[current_node]))
            current_node = prev_node[current_node]
        for direction in self.paths[start]:
            if self.paths[start][direction][0] == track[len(track) - 1][0]:
                track.append((start, direction))
        track.reverse()
        return track

