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
    comm.first_communication()  # set planet and ready -> prev & curr pos in Planet
    print('move to first node'); time.sleep(1)
    print('robot searches for next paths -> send to Planet'); time.sleep(1)
    while not comm.end_exploration:
        planet.intelligent_search()     # calc next path by Planet (intelligent search)
        print(planet.position[0][0], planet.position[0][1], planet.get_direction()); time.sleep(1)
        comm.path_select_and_result_handler(select={'Xs': int(input('nextX: ')),
                                        'Ys': int(input('nextY: ')),
                                        'Ds': int(input('nextDirection: '))})
                # send next path wanted and handle results -> send to Planet
        print('Robot gets next path from Planet (check if target available/server/else) and goes there'); time.sleep(1)
        print('process data from the drive in odometry'); time.sleep(1)
        print('robot searches for next paths -> send to Planet'); time.sleep(1)    # apply odometry after each movement!
        # planet.discover_paths(((int(input('nodeX: ')),
        #                       int(input('nodeY: '))),
        #                      Direction(int(input('nodeDirection: ')))))
        comm.path_and_result_handler(path={'Xs': int(input('prevX: ')),
                                      'Ys': int(input('prevY: ')),
                                      'Ds': int(input('prevOrientation: ')),
                                      'Xe': int(input('endX: ')),
                                      'Ye': int(input('endY: ')),
                                      'De': int(input('endOrientation: ')),
                                      'pathStatus': input('pathStatus: ')})
                # send path msg and send result to Planet or end exploration
        planet.output_paths()
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
