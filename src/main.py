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
    comm.planet = planet
    if input('move awae (y/n) ') == 'y':
        while True:
            movement.moveStraight(50)
            time.sleep(0.1)
    comm.first_communication()  # set planet and ready -> prev & curr pos in Planet
    movement.moveOnLine()  # move to first node
    planet.add_path(
        ((planet.position[0][0], planet.position[0][1]), Direction(int((180 + planet.position[1].value) % 360))),
        ((planet.position[0][0], planet.position[0][1]), Direction(int((180 + planet.position[1].value) % 360))), - 1)
    # set entry path to blocked
    ev3.Sound.beep()
    planet.defineColorIdents(movement.endColor, planet.position[0][0], planet.position[0][1])
    print("same:", planet.color_same_mod2)
    print("different:", planet.color_different_mod2)
    for paths in movement.findPathsOdometry(planet.position[1].value):
        planet.discover_paths(((planet.position[0][0], planet.position[0][1]), Direction(int(paths))))
    planet.node_explored(((planet.position[0][0], planet.position[0][1]), planet.position[1]))
    # robot searches for next paths -> send to Planet
    planet.intelligent_search()  # calc next path by Planet (intelligent search)
    while not comm.end_exploration:
        print('unexplored paths: ' + str(planet.unexplored_paths))
        print('unexplored nodes: ' + str(planet.unexplored_nodes))
        print('explored nodes: ' + str(planet.explored_nodes))
        comm.path_select_and_result_handler(select={'Xs': int(planet.position[0][0]),
                                                    'Ys': int(planet.position[0][1]),
                                                    'Ds': int(planet.position[1].value)})
        # send next path wanted and handle results -> send to Planet
        movement = Movement()
        print('prevDir: ' + str(planet.prev_position[1]) + ' , planetOrientation: ' + str(planet.position[1]))
        movement.changeDirectionAbsolut(planet.prev_position[1].value, planet.position[1].value)
        planet.change_prev_position(((planet.position[0][0], planet.position[0][1]), planet.position[1]))
        movement.moveOnLine()  # Robot gets next path from Planet and goes there
        odometry = Odometry(movement.lWheelDistances,
                            movement.rWheelDistances,
                            planet.position[1].value,
                            planet.position[0][0],
                            planet.position[0][1],
                            movement.status,
                            movement.endColor,
                            planet)  # process data from the drive in odometry
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
        print('currOrientation: ' + str(planet.position[1]))
        print('currPosition: ' + str(planet.position[0]))
        if (planet.position[0][0], planet.position[0][1]) in planet.unexplored_nodes:
            ev3.Sound.beep()
            new_paths = movement.findPathsOdometry(planet.position[1].value)
            print(new_paths)
            for paths in new_paths:
                planet.discover_paths(((planet.position[0][0], planet.position[0][1]),
                                       Direction(paths)))
        # robot searches for next paths -> send to Planet
        print('currOrientation: ' + str(planet.position[1]))
        planet.node_explored(((planet.position[0][0], planet.position[0][1]), planet.position[1]))
        # set curr node to explored
        planet.change_prev_position(planet.position)  # set prev pos to curr pos
        planet.intelligent_search()  # calc next path by Planet (intelligent search)
        comm.check_exploration_complete()  # check exploration complete or target reached

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
