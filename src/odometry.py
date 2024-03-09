# !/usr/bin/env python3

import math
import time

a = 118       # space between wheels in mm, 11,8 cm, measured from mid to mid, 9 inbetween, one wheel width = 2,8
class Odometry:
    def __init__(self, lwheeldistances, rwheeldistances, prevdir):
        # Initializes odometry module
        self.lValues = lwheeldistances
        self.rValues = rwheeldistances
        self.prevDirection = 2 * math.pi * prevdir/360



    def directionDifferenceOfLine(self):
        dirChange = 0
        for i in range(len(self.lValues)):
            dirChange += self.directionDifference(self.lValues[i], self.rValues[i])
            #print(self.lValues[i], self.rValues[i])
            #print(dirChange*360/(2*math.pi))
        return dirChange * 360 / (2 * math.pi)


    def coordinateDifferenceOfLine(self):

        xDiff = 0
        yDiff = 0
        aftDirX = math.sin(self.prevDirection)
        aftDirY = math.cos(self.prevDirection)
        for i in range(len(self.lValues)):
            prevDirX = aftDirX
            prevDirY = aftDirY

            aftDirX = math.sin(prevDirX + self.directionDifference(self.lValues[i], self.rValues[i]))
            aftDirY = math.cos(prevDirY + self.directionDifference(self.lValues[i], self.rValues[i]))

            k = self.distance(self.lValues[i], self.rValues[i]) / math.sqrt((prevDirX + aftDirX) ** 2 + (prevDirY + aftDirY) ** 2)
            xDiff += k * (prevDirX + aftDirX)
            yDiff += k * (prevDirY + aftDirY)
            #if i < 20:
                #print(xDiff/500, yDiff/500)
        return xDiff / 500, yDiff / 500         # in mm, coordinates unit = 50 cm -> 1 unit = 500 mm


    def directionDifference(self, lDistance, rDistance):
        return (rDistance - lDistance) / a


    def distance(self, lDistance, rDistance):       # distance for one intervall
        if (abs(rDistance - lDistance) < 5):
            return (rDistance + lDistance) / 2
        else:
            return (a * (rDistance + lDistance) / (rDistance - lDistance) * math.sin((rDistance - lDistance) / 2 * a))