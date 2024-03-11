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
    planet = Planet()
    # robot = Robot()
    odometry = Odometry()
    comm.planet = planet
    comm.first_communication()
    print('move to first node'); time.sleep(3)
    print('set curr & prev pos of Planet to start pos set by comm'); time.sleep(3)
    while not comm.end_exploration:
        print('robot searches for next paths'); time.sleep(3)
        print('calc next path by Planet (path algo)'); time.sleep(3)
        comm.node_comm_part_two(select={'Xs': 0, 'Ys': 0, 'Ds': 0})
                # send next path taken and handle results -> send to Planet
        print('Robot gets next node from Planet (path algo) and goes there'); time.sleep(3)
        print('process data from the drive in odometry'); time.sleep(3)
        comm.node_comm_part_one(path={'Xs': 0, 'Ys': 0, 'Ds': 0, 'Xe': 0, 'Ye': 0, 'De': 0, 'pathStatus': 'free'})
                # send path msg and send result to Planet or end exploration
        pass
    comm.end_communication()  # close communication


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
