# !/usr/bin/env python3

import math

a = 50       # space between wheels in mm
class Odometry:
    def __init__(self, lwheeldistances, rwheeldistances, prevdir):
        # Initializes odometry module
        self.lValues = lwheeldistances
        self.rValues = rwheeldistances
        self.prevDirection = prevdir



    def directionDifferenceOfLine(self):
        dirChange = 0
        for i in range(len(self.lValues)):
            dirChange += self.directionDifference(self.lValues[i], self.rValues[i])
        return dirChange

    def coordinateDifferenceOfLine(self):
        xdDiff = 0
        yDiff = 0
        prevDirX = math.sin(self.prevDirection)
        prevDirY = math.cos(self.prevDirection)
        aftDirX = math.sin(self.prevDirection + self.directionDifference(self.lValues[0], self.rValues[0]))
        aftDirY = math.cos(self.prevDirection + self.directionDifference(self.lValues[0], self.rValues[0]))

        k = self.distance(self.lValues[0], self.rValues[0]) / math.sqrt((prevDirX + aftDirX) ** 2 + (prevDirY + aftDirY) ** 2)

        # calculate each true distance and degree, add all

        # approximate direction and coordinates of next node

    def directionDifference(self, lDistance, rDistance):
        return (rDistance - lDistance) / a

    def distance(self, lDistance, rDistance):       # distance for one intervall
        return (a * (rDistance + lDistance) / (rDistance - lDistance) * math.sin((rDistance - lDistance) / 2 * a))