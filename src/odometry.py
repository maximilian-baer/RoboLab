# !/usr/bin/env python3

import math
import time

# a = 118       # space between wheels in mm, 11,8 cm, measured from mid to mid, 9 inbetween, one wheel width = 2,8
a = 90
class Odometry:
    def __init__(self, lwheeldistances=[], rwheeldistances=[], prevdir=0, prevx=0, prevy=0, pathstatus="free"):
        # Initializes odometry module
        self.lValues = lwheeldistances
        self.rValues = rwheeldistances
        self.prevDirection = prevdir
        self.prevX = prevx
        self.prevY = prevy
        self.pathStatus = pathstatus


    def currentCoordinates(self):
        if(self.pathStatus == "blocked"):
            return self.prevX, self.prevY
        else:
            difference = self.coordinateDifferenceOfLine()
            return self.prevX + round(difference[0],0), self.prevY + round(difference[1],0)


    def directionDifferenceOfLine(self):
        dirChange = 0
        for i in range(len(self.lValues)):
            dirChange += self.directionDifference(self.lValues[i], self.rValues[i])
            #print(self.lValues[i], self.rValues[i])
        return dirChange * 360 / (2 * math.pi)


    def currentDirection(self):
        if self.pathStatus == "blocked":
            return (self.prevDirection + 180) % 360
        else:
            direction = (self.prevDirection) - self.directionDifferenceOfLine()
            direction = direction % 360
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
        prevDir = 2 * math.pi * ((360 - self.prevDirection)%360)/360
        xDiff = 0
        yDiff = 0
        aftDirX = -math.sin(prevDir)
        aftDirY = math.cos(prevDir)
        aftDir = prevDir
        distancesum = 0
        for i in range(len(self.lValues)):
            prevDirX = aftDirX
            prevDirY = aftDirY
            prevDir = aftDir

            dirDiff = self.directionDifference(self.lValues[i], self.rValues[i])
            aftDir = prevDir + dirDiff
            aftDirX = -math.sin(aftDir)
            aftDirY = math.cos(aftDir)

            prevDirLength = math.sqrt(prevDirX**2 + prevDirY**2)

            distance = self.distance(self.lValues[i], self.rValues[i]) / 500    # in mm, coordinates unit = 50 cm -> 1 unit = 500 mm

            xDiff += (math.cos(dirDiff/2) * prevDirX + math.sin(dirDiff/2) * (prevDirY)) * distance / prevDirLength
            yDiff += (math.cos(dirDiff/2) * prevDirY + math.sin(dirDiff/2) * (-prevDirX))  * distance / prevDirLength

        newDir = self.currentDirection()
        newDirX = -math.sin(newDir)
        newDirY = math.cos(newDir)
        return xDiff * 1.2 + 0.1 * newDirX, 1.2 * yDiff + 0.1 * newDirY      # *1.25 because 1 unit is always measured as 70 - 85



    def directionDifference(self, lDistance, rDistance):
        return ((rDistance - lDistance) / a) #* 1.2          # * 1.2 is experimental!!! knowing this is always at least 10-40° less per 90°, this is an experimental fix


    def distance(self, lDistance, rDistance):       # distance for one intervall in mm
        if abs(rDistance - lDistance) < 5:
            return (rDistance + lDistance) / 2
        else:
            return (a * (rDistance + lDistance) / (rDistance - lDistance) * math.sin((rDistance - lDistance) / 2 * a))