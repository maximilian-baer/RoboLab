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
    def __init__(self):
        """ Initializes the data structure """
        self.paths = {}

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
        self.paths[start[0][start[1]]] = {Tuple[target[0], target[1], weight]}


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

    def setPlanet(self, planetName, startX, startY, startOrientation):
        """
        sets the planet's name and startX, startY, startOrientation of the bot
        :param planetName: String
        :param startX: Int
        :param startY: Int
        :param startOrientation: Int
        :return: void
        """
        print(planetName, startX, startY, startOrientation)
        pass

    def pathSelect(self, startDirection):
        """
        sets the direction of the next path of the bot
        :param startDirection: Int
        :return: void
        """
        print(startDirection)
        pass

    def pathCorrection(self, startX, startY, startDirection, endX, endY, endDirection, pathStatus, pathWeight):
        """
        sets the actual position of start and end nodes of the path taken by the bot -> path to be added to path list
        :param startX: Int
        :param startY: Int
        :param startDirection: Int
        :param endX: Int
        :param endY: Int
        :param endDirection: Int
        :param pathStatus: "free|blocked"
        :param pathWeight: Int
        :return: void
        """
        print(startX, startY, startDirection, endX, endY, endDirection, pathStatus, pathWeight)
        pass

    def pathUnveiled(self, startX, startY, startDirection, endX, endY, endDirection, pathStatus, pathWeight):
        """
        adds new path found by the mothership
        :param startX: Int
        :param startY: Int
        :param startDirection: Int
        :param endX: Int
        :param endY: Int
        :param endDirection: Int
        :param pathStatus: "free|blocked"
        :param pathWeight: Int
        :return: void
        """
        print(startX, startY, startDirection, endX, endY, endDirection, pathStatus, pathWeight)
        pass

    def addTarget(self, targetX, targetY):
        """
        adds new Target to Target-list
        :param targetX: Int
        :param targetY: Int
        :return: void
        """
        print(targetX, targetY)
        pass

    def adjust(self, startX, startY, startDirection, endX, endY, endDirection):
        """
        dunno, just ignore ig
        :param startX: Int
        :param startY: Int
        :param startDirection: Int
        :param endX: Int
        :param endY: Int
        :param endDirection: Int
        :return: void
        """
        print(startX, startY, startDirection, endX, endY, endDirection)
        pass

