import ev3dev.ev3 as ev3
import time

class Robot:
    def __init__(self):
        self.white = 67.5  # (245, 465, 465)
        self.black = 1.5  # (30, 75, 75)
        self.rWheelDistances = []
        self.lWheelDistances = []
    def moveOnLine(self):
        self.rWheelDistances = []
        self.lWheelDistances = []

        offset = (self.white + self.black) / 2
        Kp = 2.2      # not calibrated
        Kd = 5      # not calibrated
        Tp = 200
        lastError = 0
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
        while(ultrasonicSensor.value() > 100 and not(rgb[0] > 100 and rgb[1] < 100 and rgb[2] < 50) and not(rgb[0] < 50 and rgb[1] > 100 and rgb[2] > 50)):
            Lightvalue = self.calc_luminance(rgb[0], rgb[1], rgb[2])
            error = Lightvalue - offset
            derivative = error - lastError
            Turn = Kp * error + Kd * derivative
            print(Turn)
            power_B = Tp - Turn
            power_C = Tp + Turn
            if power_B < 0: power_B = 0
            if power_C < 0: power_C = 0
            """if abs(power_B - power_C) < 5:
                power_B += 50
                power_C += 50"""
            outB.stop()
            outC.stop()
            outB.speed_sp = power_B
            outC.speed_sp = power_C
            print(power_C)
            outB.command = "run-forever"
            outC.command = "run-forever"

            lastError = error

            rgb = colorSensor.raw

            self.rWheelDistances.append(0.48 * outC.position)       # in mm !!!
            self.lWheelDistances.append(0.48 * outB.position)       # all distances from the wheels in one line

        outB.stop()
        outC.stop()

        if ultrasonicSensor.value() < 100:
            """self.rightTurn(180)
            self.moveOnLine()"""
        else:
            """an Kreuzung angekommen"""


    def rightTurn(self, degree):
        outB = ev3.LargeMotor("outB")
        outC = ev3.LargeMotor("outC")
        outB.reset()
        outC.reset()
        outB.stop_action = "brake"
        outC.stop_action = "brake"
        outB.speed_sp = 100
        outC.speed_sp = -100
        while (outB.position < degree * 2):
            outC.command = "run-forever"
            outB.command = "run-forever"
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
