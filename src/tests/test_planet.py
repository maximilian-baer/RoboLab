#!/usr/bin/env python3

import unittest
from planet import Direction, Planet


class ExampleTestPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        +--+
        |  |
        +-0,3------+
           |       |
          0,2-----2,2 (target)
           |      /
        +-0,1    /
        |  |    /
        +-0,0-1,0
           |
        (start)

        """
        # Initialize your data structure here
        self.planet = Planet()
        self.planet.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
        self.planet.add_path(((0, 1), Direction.WEST), ((0, 0), Direction.WEST), 1)
        self.planet.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
        self.planet.add_path(((1, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 1)
        self.planet.add_path(((2, 2), Direction.WEST), ((0, 2), Direction.EAST), 1)
        self.planet.add_path(((2, 2), Direction.NORTH), ((0, 3), Direction.EAST), 1)
        self.planet.add_path(((0, 1), Direction.NORTH), ((0, 2), Direction.SOUTH), 1)
        self.planet.add_path(((0, 2), Direction.NORTH), ((0, 3), Direction.SOUTH), 1)
        self.planet.add_path(((0, 3), Direction.WEST), ((0, 3), Direction.NORTH), 1)

    @unittest.skip('Example test, should not count in final test results')
    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """
        self.assertIsNone(self.planet.shortest_path((0, 0), (1, 2)))


class TestRoboLabPlanet(unittest.TestCase):
    def setUp(self):
        """
        Instantiates the planet data structure and fills it with paths

        MODEL YOUR TEST PLANET HERE (if you'd like):

        """
        # Initialize your data structure here
        self.planet = Planet()
        self.planet.add_path(start=((1, 1), Direction.EAST), target=((3, 1), Direction.WEST), weight=6)
        self.planet.add_path(start=((1, 1), Direction.SOUTH), target=((1, 4), Direction.NORTH), weight=2)
        self.planet.add_path(start=((1, 4), Direction.EAST), target=((3, 1), Direction.SOUTH), weight=3)
        self.planet.add_path(start=((3, 1), Direction.EAST), target=((5, 1), Direction.WEST), weight=4)
        self.planet.add_path(start=((3, 1), Direction.NORTH), target=((4, 3), Direction.NORTH), weight=1)
        self.planet.add_path(start=((5, 1), Direction.SOUTH), target=((5, 5), Direction.NORTH), weight=5)
        self.planet.add_path(start=((1, 4), Direction.SOUTH), target=((5, 5), Direction.WEST), weight=4)
        self.planet.add_path(start=((4, 3), Direction.SOUTH), target=((5, 5), Direction.SOUTH), weight=4)
        self.planet.add_path(start=((1, 1), Direction.NORTH), target=((1, 1), Direction.WEST), weight=4)
        self.planet.add_path(start=((1, 1), Direction.NORTH), target=((1, 1), Direction.WEST), weight=5)
        # self.planet.add_path(...)

    def test_integrity(self):
        """
        This test should check that the dictionary returned by "planet.get_paths()" matches the expected structure
        """
        print(self.planet.get_paths())

    def test_empty_planet(self):
        """
        This test should check that an empty planet really is empty
        """
        self.planet = Planet()
        n_paths = len(self.planet.get_paths())
        print(n_paths)

    def test_target(self):
        """
        This test should check that the shortest-path algorithm implemented works.

        Requirement: Minimum distance is three nodes (two paths in list returned)
        """
        print(self.planet.shortest_path((1, 1), (5, 5)))

    def test_target_not_reachable(self):
        """
        This test should check that a target outside the map or at an unexplored node is not reachable
        """
        self.planet.add_path(start=((1, 4), Direction.SOUTH), target=((5, 5), Direction.WEST), weight=-1)
        self.planet.add_path(start=((4, 3), Direction.SOUTH), target=((5, 5), Direction.SOUTH), weight=-1)
        self.planet.add_path(start=((1, 1), Direction.NORTH), target=((1, 1), Direction.WEST), weight=-1)
        print(self.planet.shortest_path((1, 1), (5, 5)) is None)

    def test_same_length(self):
        """
        This test should check that the shortest-path algorithm implemented returns a shortest path even if there
        are multiple shortest paths with the same length.

        Requirement: Minimum of two paths with same cost exists, only one is returned by the logic implemented
        """
        self.planet.add_path(start=((1, 4), Direction.SOUTH), target=((5, 5), Direction.WEST), weight=9)
        print(self.planet.shortest_path((1, 1), (5, 5)))

    def test_target_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target nearby

        Result: Target is reachable
        """
        self.planet.add_path(start=((3, 1), Direction.NORTH), target=((3, 1), Direction.NORTH), weight=1)
        print(self.planet.shortest_path((0, 0), (5, 5)))

    def test_target_not_reachable_with_loop(self):
        """
        This test should check that the shortest-path algorithm does not get stuck in a loop between two points while
        searching for a target not reachable nearby

        Result: Target is not reachable
        """
        self.planet.add_path(start=((1, 4), Direction.SOUTH), target=((5, 5), Direction.WEST), weight=-1)
        self.planet.add_path(start=((4, 3), Direction.SOUTH), target=((5, 5), Direction.SOUTH), weight=-1)
        self.planet.add_path(start=((1, 1), Direction.NORTH), target=((1, 1), Direction.WEST), weight=-1)
        print(self.planet.shortest_path((0, 0), (5, 5)) is None)


if __name__ == "__main__":
    unittest.main()
