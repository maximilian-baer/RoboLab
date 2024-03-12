# !/usr/bin/env python3

import math
import time

# a = 118       # space between wheels in mm, 11,8 cm, measured from mid to mid, 9 inbetween, one wheel width = 2,8
a = 90
class Odometry:
    def __init__(self, lwheeldistances, rwheeldistances, prevdir, prevx, prevy):
        # Initializes odometry module
        self.lValues = lwheeldistances
        self.rValues = rwheeldistances
        self.prevDirection = 2 * math.pi * prevdir/360
        self.prevX = prevx
        self.prevY = prevy


    def currentCoordinates(self):
        difference = self.coordinateDifferenceOfLine()
        return self.prevX + round(difference[0],0), self.prevY + round(difference[1],0)


    def directionDifferenceOfLine(self):
        dirChange = 0
        for i in range(len(self.lValues)):
            dirChange += self.directionDifference(self.lValues[i], self.rValues[i])
            #print(self.lValues[i], self.rValues[i])
        return dirChange * 360 / (2 * math.pi)


    def currentDirection(self):
        direction = (self.prevDirection) - self.directionDifferenceOfLine()
        direction = direction % 360
        print(direction, self.prevDirection, self.directionDifferenceOfLine())
        if (direction <= 45 or direction > 315):
            return 0
        elif (direction <= 135):
            return 90
        elif (direction <= 225):
            return 180
        elif (direction <= 315):
            return 270
        else:
            return direction


    def coordinateDifferenceOfLine(self):

        xDiff = 0
        yDiff = 0
        aftDirX = math.sin(self.prevDirection)
        aftDirY = math.cos(self.prevDirection)
        aftDir = self.prevDirection
        distancesum = 0
        for i in range(len(self.lValues)):
            prevDirX = aftDirX
            prevDirY = aftDirY
            prevDir = aftDir

            dirDiff = self.directionDifference(self.lValues[i], self.rValues[i])
            aftDir = prevDir + dirDiff
            aftDirX = math.sin(aftDir)
            aftDirY = math.cos(aftDir)

            prevDirLength = math.sqrt(prevDirX**2 + prevDirY**2)

            distance = self.distance(self.lValues[i], self.rValues[i]) / 500    # in mm, coordinates unit = 50 cm -> 1 unit = 500 mm

            xDiff += (math.cos(dirDiff/2) * prevDirX + math.sin(dirDiff/2) * (-prevDirY)) * distance / prevDirLength
            yDiff += (math.cos(dirDiff/2) * prevDirY + math.sin(dirDiff/2) * (prevDirX))  * distance / prevDirLength

        return xDiff, yDiff


    def directionDifference(self, lDistance, rDistance):
        return ((rDistance - lDistance) / a) #* 1.2          # * 1.2 is experimental!!! knowing this is always at least 10-40° less per 90°, this is an experimental fix


    def distance(self, lDistance, rDistance):       # distance for one intervall in mm
        if abs(rDistance - lDistance) < 5:
            return (rDistance + lDistance) / 2
        else:
            return (a * (rDistance + lDistance) / (rDistance - lDistance) * math.sin((rDistance - lDistance) / 2 * a))