#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
from enum import IntEnum, unique
from typing import Optional, List, Tuple, Dict


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
    def __init__(self, planet_name: str, start: Tuple[Tuple[int, int], Direction]):
        """ Initializes the data structure """
        self.planet_name = planet_name
        self.paths = {}
        self.add_path(start=start)
        self.targets = []
        self.position = [Tuple[start[0][0], start[0][1]], start[1]]
        self.prev_position = []

    def exploration_complete(self) -> bool:
        """
        gets if exploration is complete
        :return: boolean
        """
        pass

    def path_select(self):
        """
        sets the direction of the next path of the bot
        :param startDirection: Int
        :return: void
        """
        pass

    def path_unveiled(self):
        pass

    def change_position(self, start: Tuple[Tuple[int, int], Direction]):
        self.prev_position = self.prev_position
        self.position = [list(start[0]), Direction]

    def receive_target(self, target: Tuple[int, int]):
        if target not in self.paths:
            self.paths[target] = {}

        self.targets.append(target)

    def on_target(self) -> bool:
        for target in self.targets:
            if self.position == list(target):
                return True
        return False

    def discover_paths(self, v, direction):
        self.paths[v][direction] = ((None, None), None, None)

    # DO NOT EDIT THE METHOD SIGNATURE
    def add_path(self, start: Tuple[Tuple[int, int], Direction], target: Tuple[Tuple[int, int], Direction] = None,
                 weight: int = None):
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
        if target is not None and target[0] not in self.paths:
            self.paths[target[0]] = {}
        if target is not None:
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

    def explore_closest_path(self, start, target):
        track = self.shortest_path(start, target)
        if track is None:
            return



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


    # DO NOT EDIT THE METHOD SIGNATURE
    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]) -> Optional[
        List[Tuple[Tuple[int, int], Direction]]]:
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
        # in case the vertex has to path yet
        if target not in self.paths or self.paths[target] == {}:
            return None
        # variable for backtracking
        track = []
        # dictionary for saving previous node for backtracking
        prev_node = {}
        # set of remaining vertices
        vertices = set()
        # initiate vertices
        c_paths = list(self.paths.keys())
        for i in range(len(self.paths)):
            vertices.add(c_paths[i])
        # dictionary for corresponding weight values (infinite at the beginning)
        distances = {v: float('inf') for v in vertices}
        distances[start] = 0
        # as long as there are not calculated vertices left
        while len(vertices) > 0:
            v = self.get_closest_vertex(vertices, distances)
            # in case all remaining vertices are not reachable
            if distances[v] == float('inf'):
                return None
            # or the target is calculated (to prevent redundant operations)
            elif v == target:
                break
            vertices.remove(v)
            # foreach element next to v
            for w in self.get_neighbours(v, vertices):
                # new costs being calculated
                new_distance = distances[v] + w[1]
                # if path via v is shorter than previous length of path
                if new_distance < distances[w[0]]:
                    distances[w[0]] = new_distance
                    prev_node[w[0]] = v
        # backtracking
        track.append(target)
        current_node = target
        while current_node != start:
            for direction in self.paths[prev_node[current_node]]:
                if self.paths[prev_node[current_node]][direction][0] == current_node:
                    track.append((prev_node[current_node], direction))
            current_node = prev_node[current_node]
        track.reverse()
        return track
