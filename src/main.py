#!/usr/bin/env python3
import ev3dev.core
import json
import ev3dev.ev3 as ev3

import logging
import os
import paho.mqtt.client as mqtt
import uuid
import signal
import time
import threading

from communication import Communication
from odometry import Odometry
from planet import Direction, Planet

client = None  # DO NOT EDIT


def run():
    # DO NOT CHANGE THESE VARIABLES
    #
    # The deploy-script uses the variable "client" to stop the mqtt-client after your program stops or crashes.
    # Your script isn't able to close the client after crashing.
    global client

    client_id = '013-' + str(uuid.uuid4())  # Replace YOURGROUPID with your group ID
    client = mqtt.Client(client_id=client_id,  # Unique Client-ID to recognize our program
                         clean_session=True,  # We want a clean session after disconnect or abort/crash
                         protocol=mqtt.MQTTv311  # Define MQTT protocol version
                         )
    # Setup logging directory and file
    curr_dir = os.path.abspath(os.getcwd())
    if not os.path.exists(curr_dir + '/../logs'):
        os.makedirs(curr_dir + '/../logs')
    log_file = curr_dir + '/../logs/project.log'
    logging.basicConfig(filename=log_file,  # Define log file
                        level=logging.DEBUG,  # Define default mode
                        format='%(asctime)s: %(message)s'  # Define default logging format
                        )
    logger = logging.getLogger('RoboLab')

    # THE EXECUTION OF ALL CODE SHALL BE STARTED FROM WITHIN THIS FUNCTION.
    # ADD YOUR OWN IMPLEMENTATION HEREAFTER.
    comm = Communication(client, logger)
    comm.planet = Planet()
    comm.connect()
    comm.listen('explorer/013')
    comm.disconnect()

    print("Hello World!")

    """m = ev3.LargeMotor("outB")
    m.reset()
    m.stop_action = "brake"
    m.speed_sp = 100
    m.command = "run-forever"
    time.sleep(3)

    m.speed_sp = 200
    m.command = "run-forever"
    time.sleep(3)
    m.stop()"""

    """for i in range(10):
        cs = ev3.ColorSensor()
        cs.mode = 'COL-REFLECT'
        print(cs.reflected_light_intensity)
        time.sleep(0.1)"""

    moveOnLine()


def moveOnLine():
    white = 74
    black = 10
    offset = 42
    Kp = 5
    Tp = 150
    colorSensor = ev3.ColorSensor()
    colorSensor.mode = 'COL-REFLECT'
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
    i = 0
    """while(ultrasonicSensor.value() > 100 and i < 20):
            Lightvalue = colorSensor.reflected_light_intensity
            error = Lightvalue - offset
            Turn = Kp * error
            powe
            r_B = Tp - Turn
            power_C = Tp + Turn
            outB.speed_sp = power_B
            c.speed_sp = power_C
            #print(ultrasonicSensor.value())
            print(Lightvalue)
            #time.sleep(1)
            #i += 1"""
    time.sleep(2)
    outB.stop()
    outB.speed_sp = 200
    outB.command = "run-forever"
    outC.stop()
    outC.speed_sp = 100
    outC.command = "run-forever"
    time.sleep(2)
    outB.stop()
    outB.speed_sp = 150
    outB.command = "run-forever"
    outC.stop()
    outC.speed_sp = 150
    outC.command = "run-forever"
    time.sleep(2)
    outB.speed_sp = 100
    outB.command = "run-forever"
    outC.speed_sp = 200
    outC.command = "run-forever"
    time.sleep(2)

    outB.stop()
    outC.stop()


# DO NOT EDIT
def signal_handler(sig=None, frame=None, raise_interrupt=True):
    if client and client.is_connected():
        client.disconnect()
    if raise_interrupt:
        raise KeyboardInterrupt()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    try:
        run()
        signal_handler(raise_interrupt=False)
    except Exception as e:
        signal_handler(raise_interrupt=False)
        raise e
