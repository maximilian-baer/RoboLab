#!/usr/bin/env python3
import time
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
        self.explored_nodes = []
        self.paths = {}
        self.target = None
        self.position = [[0, 0], Direction.NORTH]
        self.prev_position = []
        self.path_target = []
        self.unexplored_paths = []
        self.unexplored_nodes = []

    def exploration_complete(self) -> bool:
        """
        gets if exploration is complete
        :return: boolean
        """
        if len(self.unexplored_paths) == 0 and len(self.unexplored_nodes) == 0:
            return True
        return False

    def intelligent_search(self):
        print('start intelligent search... ')
        if len(self.path_target) > 0:
            print('got target path ')
            print('path: ', self.path_target)
            next_node = self.path_target.pop(0)
            self.change_position((next_node[0], next_node[1]))
        else:
            if len(self.unexplored_paths) > 0 and self.unexplored_paths_reachable():
                print('unexplored paths found: ' + str(self.unexplored_paths))
                v_min = self.unexplored_paths[0]
                distance_min = self.distance_to((self.position[0][0], self.position[0][1]), v_min)
                for path in self.unexplored_paths:
                    new_distance = self.distance_to(start=(self.position[0][0], self.position[0][1]), target=path[0])
                    if distance_min > new_distance:
                        v_min = path
                        distance_min = new_distance
                if (self.position[0][0], self.position[0][1]) == v_min[0]:
                    self.change_position(v_min)
                elif self.shortest_path((self.position[0][0], self.position[0][1]), v_min[0]) is None:
                    print('Planet.intelligent_search: shortest_path to unexplored path is None: ' +
                          str((self.position[0][0], self.position[0][1])) +
                          ' -> ' +
                          str(v_min[0]))
                else:
                    self.change_position(((self.position[0][0], self.position[0][1]),
                                          self.shortest_path((self.position[0][0], self.position[0][1]), v_min[0])[0][
                                              1]))

            elif len(self.unexplored_nodes) > 0:
                print('len(planet.unexplored_paths) = ' + str(len(self.unexplored_paths)))
                print('planet.unexplored_paths_reachable() = ' + str(self.unexplored_paths_reachable()))
                print('unexplored paths: ' + str(self.unexplored_paths))
                print('unexplored nodes found: ' + str(self.unexplored_nodes))
                v_min = self.unexplored_nodes[0]
                distance_min = self.distance_to((self.position[0][0], self.position[0][1]), v_min)
                for node in self.unexplored_nodes:
                    new_distance = self.distance_to(start=(self.position[0][0], self.position[0][1]), target=node)
                    if distance_min > new_distance:
                        v_min = node
                        distance_min = new_distance
                print('distance to min unexplored node: ' + str((self.position[0][0], self.position[0][1])) + ' -> ' + str(v_min) +
                      ' = ' + str(self.distance_to((self.position[0][0], self.position[0][1]), v_min)))
                if self.distance_to((self.position[0][0], self.position[0][1]), v_min) == float('inf'):
                    self.unexplored_nodes = []
                    self.unexplored_paths = []
                    print('killed all paths and nodes')
                else:
                    if (self.position[0][0], self.position[0][1]) == v_min:
                        print('Planet.intelligent_search: on unexplored node!')
                    elif self.shortest_path((self.position[0][0], self.position[0][1]), v_min[0]) is None:
                        print('Planet.intelligent_search: shortest_path to unexplored node is None: ' +
                              str((self.position[0][0], self.position[0][1])) +
                              ' -> ' +
                              str(v_min))
                    else:
                        self.change_position(((self.position[0][0], self.position[0][1]),
                                              self.shortest_path((self.position[0][0], self.position[0][1]), v_min)[0][
                                                  1]))
            else:
                print('Planet.intelligent_search: no unexorabled entities left: nodes: ' + str(
                    self.unexplored_nodes) + ' , paths: ' + str(self.unexplored_paths))
        print('stop intelligent search... ')

    def change_position(self, start: Tuple[Tuple[int, int], Direction]):
        self.prev_position = self.position
        self.position = [list(start[0]), start[1]]

    def receive_target(self, target: Tuple[int, int]):
        if target not in self.unexplored_nodes and target not in self.explored_nodes:
            self.unexplored_nodes.append(target)
        if target not in self.paths:
            self.paths[target] = {}

        self.target = target

    def discover_paths(self, node: Tuple[Tuple[int, int], Direction]):
        if node[1] not in self.paths[node[0]] and node not in self.unexplored_paths:
            self.add_path(start=node)
            self.unexplored_paths.append(node)

    def node_explored(self, node: Tuple[Tuple[int, int], Direction]):
        if node[0] in self.unexplored_nodes and node[0] not in self.explored_nodes:
            self.unexplored_nodes.remove(node[0])
            self.explored_nodes.append(node[0])


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
        print('adding path: ' + str(start) + ' -> ' + str(target))

        # target is not None and
        if self.target is not None and self.shortest_path((self.position[0][0], self.position[0][1]), (self.target[0], self.target[1])) is not None:
            print('add target path: ' + str((self.position[0][0], self.position[0][1])) + ' -> ' + str(self.target) +
                  'with weight: ' + str(self.distance_to((self.position[0][0], self.position[0][1]), (self.target[0], self.target[1]))))
            self.path_target = self.shortest_path((self.position[0][0], self.position[0][1]), (self.target[0], self.target[1]))
        if (start in self.path_target or target in self.path_target) and weight == -1:
            self.path_target = []
            print('reset path_target')
        if start in self.unexplored_paths and target is not None:
            self.unexplored_paths.remove(start)
        # if target is not None and target[0] not in self.explored_nodes and target[0] not in self.unexplored_nodes:
        #     self.unexplored_nodes.append(target[0])
        if target is not None and target in self.unexplored_paths:
            self.unexplored_paths.remove(target)
        if start[0] not in self.paths:
            self.paths[start[0]] = {}
        if target is not None and target[0] not in self.paths:
            self.paths[target[0]] = {}
        if target is not None:
            self.paths[start[0]][start[1]] = (target[0], target[1], weight)
            self.paths[target[0]][target[1]] = (start[0], start[1], weight)

    def set_planet(self, planetName, startX, startY, startOrientation):
        """
        sets the planet's name and startX, startY, startOrientation of the bot
        :param planetName: String
        :param startX: Int
        :param startY: Int
        :param startOrientation: Int
        :return: void
        """
        self.add_path(start=((startX, startY), Direction(startOrientation)))
        self.position = [[startX, startY], startOrientation]
        self.change_position(((startX, startY), Direction(int(startOrientation))))

    def path_select(self, startDirection):
        """
        sets the direction of the next path of the bot
        :param startDirection: Int
        :return: void
        """
        if not (len(self.path_target) > 0):
            self.change_position(((self.position[0][0], self.position[0][1]), Direction(int(startDirection))))

    def path_correction(self, startX, startY, startDirection, endX, endY, endDirection, pathStatus, pathWeight):
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
        self.add_path(start=((startX, startY), Direction(startDirection)), target=((endX, endY), Direction(endDirection)), weight=pathWeight)

    def path_unveiled(self, startX, startY, startDirection, endX, endY, endDirection, pathStatus, pathWeight):
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
        start = ((startX, startY), Direction(startDirection))
        target = ((endX, endY), Direction(endDirection))
        self.add_path(start, target, weight=pathWeight)
        if start[0] not in self.unexplored_nodes and start[0] not in self.explored_nodes:
            self.unexplored_nodes.append(start[0])
        if target[0] not in self.unexplored_nodes and target[0] not in self.explored_nodes:
            self.unexplored_nodes.append(target[0])

    def change_target(self, targetX, targetY):
        """
        adds new Target to Target-list
        :param targetX: Int
        :param targetY: Int
        :return: void
        """
        self.receive_target(target=(targetX, targetY))

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

    def output_paths(self):
        for v in self.paths.keys():
            print(v, self.paths[v])


    def on_target(self) -> bool:
        """
        gets if bot is on a target
        :return: boolean
        """
        if self.position[0] == self.target:
            return True
        return False

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

    def distance_to(self, start, target):
        track = self.shortest_path(start=start, target=target)
        distance = 0
        if track is None:
            return float('inf')
        for v in track:
            distance += self.paths[v[0]][v[1]][2]
        return distance



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
        current_node = target
        while current_node != start:
            for direction in self.paths[prev_node[current_node]]:
                if self.paths[prev_node[current_node]][direction][0] == current_node:
                    track.append((prev_node[current_node], direction))
            current_node = prev_node[current_node]
        track.reverse()
        return track

    def unexplored_paths_reachable(self) -> bool:
        reachable = False
        for paths in self.unexplored_paths:
            if self.shortest_path((self.position[0][0], self.position[0][1]), paths[0]) is not None:
                reachable = True
                break
            if paths[0] == (self.position[0][0], self.position[0][1]):
                reachable = True
                break
        print('unexplored paths reachable: ' + str(reachable))
        return reachable


