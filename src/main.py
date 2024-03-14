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
import asyncio

from communication import Communication
from odometry import Odometry
from planet import Direction, Planet
from movement import Movement

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
    movement = Movement()
    # odometry = Odometry()
    comm.planet = planet
    comm.first_communication()  # set planet and ready -> prev & curr pos in Planet
    movement.moveOnLine()   # move to first node
    planet.add_path(((planet.position[0][0], planet.position[0][1]), Direction( int((180 + planet.position[1].value) % 360))),
                    ((planet.position[0][0], planet.position[0][1]), Direction( int((180 + planet.position[1].value) % 360))), - 1)
            # block first path
    print('prevDir: ' + str(planet.position[1].value)); time.sleep(5)
    for paths in movement.findPathsOdometry(planet.position[1].value):  # robot searches for next paths -> send to Planet
        planet.discover_paths(((planet.position[0][0], planet.position[0][1]), Direction(int(paths))))
    prevDir = planet.position[1].value
    planet.node_explored(((planet.position[0][0], planet.position[0][1]), planet.position[1]))
    planet.intelligent_search()  # calc next path by Planet (intelligent search)
    while not comm.end_exploration:
        print('unexplored paths: ' + str(planet.unexplored_paths))
        print('unexplored nodes: ' + str(planet.unexplored_nodes))
        print('explored nodes: ' + str(planet.explored_nodes))
        comm.path_select_and_result_handler(select={'Xs': int(planet.position[0][0]),
                                                    'Ys': int(planet.position[0][1]),
                                                    'Ds': int(planet.position[1].value)})
        # send next path wanted and handle results -> send to Planet
        planet.intelligent_search()     # check if target available/server select/else
        movement.changeDirectionAbsolut(prevDir, planet.position[1].value)
        movement.moveOnLine()   # Robot gets next path from Planet and goes there
        odometry = Odometry(movement.lWheelDistances,
                            movement.rWheelDistances,
                            planet.position[1].value,
                            planet.position[0][0],
                            planet.position[0][1],
                            movement.status)    # process data from the drive in odometry
        prevDir = int(odometry.currentDirection())
        planet.change_position(((int(odometry.currentCoordinates()[0]), int(odometry.currentCoordinates()[1])),
                                Direction(int(odometry.currentDirection()))))
        comm.path_and_result_handler(path={'Xs': int(planet.prev_position[0][0]),
                                           'Ys': int(planet.prev_position[0][1]),
                                           'Ds': int(planet.prev_position[1]),
                                           'Xe': int(planet.position[0][0]),
                                           'Ye': int(planet.position[0][1]),
                                           'De': int((180 + int(planet.position[1])) % 360),
                                           'pathStatus': movement.status})
        # send path msg and send result to Planet
        print('unexplored paths: ' + str(planet.unexplored_paths))
        print('unexplored nodes: ' + str(planet.unexplored_nodes))
        print('explored nodes: ' + str(planet.explored_nodes))
        if (planet.position[0][0], planet.position[0][1]) in planet.unexplored_nodes:
            for paths in movement.findPathsOdometry(planet.position[1].value):  # robot searches for next paths -> send to Planet
                planet.discover_paths(((planet.position[0][0], planet.position[0][1]),
                                       Direction(paths)))  # Direction(int(input('nodeDirection: ')))
        planet.node_explored(((planet.position[0][0], planet.position[0][1]), planet.position[1]))
        planet.intelligent_search()  # calc next path by Planet (intelligent search)
        comm.check_exploration_complete()   # check exploration complete or target reached
        if input('continue? (y/n) ') == 'n':
            comm.end_exploration = True
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


