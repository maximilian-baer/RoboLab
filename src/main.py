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
    print("Hello World!")
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
        cs = ev3.ColorSensor()
        cs.mode = 'COL-REFLECT'
        us = ev3.UltrasonicSensor()
        us.mode = 'US-DIST-CM'

        b = ev3.LargeMotor("outB")
        b.reset()
        b.stop_action = "coast"
        b.speed_sp = Tp
        c = ev3.LargeMotor("outC")
        c.reset()
        c.stop_action = "coast"
        c.speed_sp = Tp
        b.command = "run-forever"
        c.command = "run-forever"
        i = 0
        """while(us.value() > 100 and i < 20):
            Lightvalue = cs.reflected_light_intensity
            error = Lightvalue - offset
            Turn = Kp * error
            powe
            r_B = Tp - Turn
            power_C = Tp + Turn
            b.speed_sp = power_B
            c.speed_sp = power_C
            #print(us.value())
            print(Lightvalue)
            #time.sleep(1)
            #i += 1"""
        time.sleep(2)
        b.stop()
        b.speed_sp = 200
        b.command = "run-forever"
        c.stop()
        c.speed_sp = 100
        c.command = "run-forever"
        time.sleep(2)
        b.stop()
        b.speed_sp = 150
        b.command = "run-forever"
        c.stop()
        c.speed_sp = 150
        c.command = "run-forever"
        time.sleep(2)
        b.speed_sp = 100
        b.command = "run-forever"
        c.speed_sp = 200
        c.command = "run-forever"
        time.sleep(2)

        b.stop()
        c.stop()









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
