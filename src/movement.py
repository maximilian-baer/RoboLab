import ev3dev.ev3 as ev3
import time
from odometry import Odometry
from planet import Planet

dpt = 0.48      # distance per tick

class Movement:
    def __init__(self):
        self.white = 50 #67.5  # (245, 465, 465)
        self.black = 1.5  # (30, 75, 75)
        self.rWheelDistances = []
        self.lWheelDistances = []
        self.status = "free"

    def moveOnLine(self):
        self.rWheelDistances = []
        self.lWheelDistances = []

        offset = (self.white + self.black) / 2
        Kp = 3      # calibrated
        Ki = 0.07               # (for now)
        Kd = 4.5      # calibrated
        Tp = 180
        lastError = 0
        integral = 0
        derivativ = 0
        colorSensor = ev3.ColorSensor()
        colorSensor.mode = 'RGB-RAW'
        ultrasonicSensor = ev3.UltrasonicSensor()
        ultrasonicSensor.mode = 'US-DIST-CM'

        outB = ev3.LargeMotor("outB")
        outB.reset()
        outB.stop_action = "coast"
        outB.speed_sp = Tp
        outC = ev3.LargeMotor("outC")
        outC.reset()
        outC.stop_action = "coast"
        outC.speed_sp = Tp
        outB.command = "run-forever"
        outC.command = "run-forever"
        rgb = colorSensor.raw
        lastPositionB = 0
        lastPositionC = 0

        while(ultrasonicSensor.value() > 150 and not(rgb[0] > 100 and rgb[1] < 100 and rgb[2] < 50) and not(rgb[0] < 50 and rgb[1] > 100 and rgb[2] > 50)):
            Lightvalue = self.calc_luminance(rgb[0], rgb[1], rgb[2])
            error = Lightvalue - offset
            integral += error
            derivative = error - lastError
            Turn = Kp * error + Kd * derivative + Ki * integral

            power_B = Tp - Turn
            power_C = Tp + Turn
            if power_B < 0: power_B = 0
            if power_C < 0: power_C = 0
            """if abs(power_B - power_C) < 40:
                power_B = 200
                power_C = 200"""
            outB.speed_sp = power_B
            outC.speed_sp = power_C

            outB.command = "run-forever"
            outC.command = "run-forever"

            lastError = error

            rgb = colorSensor.raw

            self.rWheelDistances.append(dpt * (outC.position-lastPositionC))       # in mm !!!
            self.lWheelDistances.append(dpt * (outB.position-lastPositionB))       # all distances from the wheels in one line
            lastPositionC = outC.position
            lastPositionB = outB.position

        if ultrasonicSensor.value() < 150:
            self.status = "blocked"
            self.TurnClockwise(175)
            self.TurnClockwise(15)
            self.moveOnLine()
        else:
            # an Kreuzung angekommen
            self.moveStraight(7.5)

    def TurnClockwise(self, degree):
        outB = ev3.LargeMotor("outB")
        outC = ev3.LargeMotor("outC")
        outB.reset()
        outC.reset()
        self.lWheelDistances = []
        self.rWheelDistances = []
        outB.stop_action = "brake"
        outC.stop_action = "brake"
        outB.speed_sp = 100
        outC.speed_sp = -100
        k = 1.9
        if degree > 180 and degree < 360:
            outB.speed_sp = -100
            outC.speed_sp = 100
            k = 1.83
            degree = degree - 180
        outC.command = "run-forever"
        outB.command = "run-forever"
        i = 0
        lastPositionB = 0
        lastPositionC = 0
        while (outB.position < degree * k and outC.position < degree * k):
            self.rWheelDistances.append(dpt * (outC.position - lastPositionC))  # in mm !!!
            self.lWheelDistances.append(dpt * (outB.position - lastPositionB))
            lastPositionC = outC.position
            lastPositionB = outB.position
        outB.stop()
        outC.stop()

    def moveStraight(self, cm):
        outB = ev3.LargeMotor("outB")
        outC = ev3.LargeMotor("outC")
        outB.reset()
        outC.reset()
        self.testlWheelDistances = []
        self.testrWheelDistances = []
        outB.stop_action = "brake"
        outC.stop_action = "brake"
        outB.speed_sp = 150
        outC.speed_sp = 150
        outC.command = "run-forever"
        outB.command = "run-forever"
        i = 0
        lastPositionB = 0
        lastPositionC = 0
        while (outB.position < cm * 10 / dpt and outC.position < cm * 10 / dpt):
            # i += (outB.position - lastPositionB)
            self.testrWheelDistances.append(dpt * (outC.position - lastPositionC))  # in mm !!!
            self.testlWheelDistances.append(dpt * (outB.position - lastPositionB))
            lastPositionC = outC.position
            lastPositionB = outB.position
            time.sleep(0.1)
        outB.stop()
        outC.stop()

    def calc_luminance(self, r, g, b):
        r = r / 512
        g = g / 512
        b = b / 512

        if r < 0.0393:
            r = (r / 12.92)
        else:
            r = ((r + 0.055) / 1.055) ** 2.4
        if g < 0.0393:
            g = (g / 12.92)
        else:
            g = ((g + 0.055) / 1.055) ** 2.4
        if b < 0.0393:
            b = (b / 12.92)
        else:
            b = ((b + 0.055) / 1.055) ** 2.4

        y = 0.2126 * r + 0.7152 * g + 0.0722 * b
        return y * 100

    def currentBrightness(self):
        colorSensor = ev3.ColorSensor()
        colorSensor.mode = 'RGB-RAW'
        listValues = []
        for i in range(10):
            listValues.append(colorSensor.raw)
            time.sleep(0.1)
        red = 0
        green = 0
        blue = 0
        for i in range(10):
            red += listValues[i][0]
            green += listValues[i][1]
            blue += listValues[i][2]
        red = red/10
        green = green/10
        blue = blue/10
        brightness = self.calc_luminance(red, green, blue)
        print(brightness)
        return brightness


    def findPathsOdometry(self, prevdir):
        done = False
        paths = []
        colorSensor = ev3.ColorSensor()
        colorSensor.mode = 'RGB-RAW'

        outB = ev3.LargeMotor("outB")
        outC = ev3.LargeMotor("outC")
        outB.reset()
        outC.reset()
        outB.stop_action = "brake"
        outC.stop_action = "brake"
        outB.speed_sp = 100
        outC.speed_sp = -100

        newPrevDir = prevdir
        odometry = Odometry(self.lWheelDistances, self.rWheelDistances, newPrevDir, 0, 0)
        while not done:
            self.lWheelDistances = []
            self.rWheelDistances = []
            outB.position = 0
            outC.position = 0
            outC.command = "run-forever"
            outB.command = "run-forever"

            lastPositionC = 0
            lastPositionB = 0
            while (outB.position < 60):
                self.rWheelDistances.append(dpt * (outC.position - lastPositionC))  # in mm !!!
                self.lWheelDistances.append(dpt * (outB.position - lastPositionB))
                lastPositionC = outC.position
                lastPositionB = outB.position
            rgb = colorSensor.raw
            while (rgb[0] > 50 or rgb[1] > 200 or rgb[2] > 50):
                self.rWheelDistances.append(dpt * (outC.position - lastPositionC))  # in mm !!!
                self.lWheelDistances.append(dpt * (outB.position - lastPositionB))
                lastPositionC = outC.position
                lastPositionB = outB.position
                rgb = colorSensor.raw
            outB.stop()
            outC.stop()
            odometry.lValues = self.lWheelDistances
            odometry.rValues = self.rWheelDistances
            odometry.prevDirection = newPrevDir
            direction = odometry.currentDirection()
            #print(odometry.lValues)
            """print("prev:", newPrevDir)
            print("diff:", odometry.directionDifferenceOfLine())
            print("new:", direction)"""
            if direction not in paths:
                paths.append(direction)
                newPrevDir = direction
            else:
                done = True
            if direction == prevdir:
                done = True

        self.changeDirectionAbsolut(direction, prevdir)

        print(paths)
        return paths


    def changeDirectionAbsolut(self, prevDir, newDir):
        while prevDir != newDir:
            self.TurnClockwise(90)
            prevDir += 90
            prevDir = prevDir % 360



    # not in use, will probably be deleted
    def findPaths90Turn(self, prevDir):
        paths = []
        colorSensor = ev3.ColorSensor()
        colorSensor.mode = 'RGB-RAW'
        for i in range(4):
            rgb = colorSensor.raw
            if rgb[1] < 200:
                paths.append((i * 90 + prevDir) % 360)
            self.perfectTurn(90)
        return paths


    def perfectTurn(self, degree):
        """turn exactly x degrees"""