#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import paho.mqtt.client as mqtt
import ssl
import time
from planet import Planet


class Communication:
    """
    Class to hold the MQTT client communication
    Feel free to add functions and update the constructor to satisfy your requirements and
    thereby solve the task according to the specifications
    """

    # DO NOT EDIT THE METHOD SIGNATURE
    def __init__(self, mqtt_client, logger):
        """
        Initializes communication module, connect to server, subscribe, etc.
        :param mqtt_client: paho.mqtt.client.Client
        :param logger: logging.Logger
        """
        # DO NOT CHANGE THE SETUP HERE
        self.client = mqtt_client
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)
        self.client.on_message = self.safe_on_message_handler
        # Add your client setup here
        self.received_msg = False
        self.planetName = None
        self.client.username_pw_set('013', password='F8mVbzVCC4')
        self.logger = logger
        self.planet = None
        self.expl = 'explorer/013'
        self.end_exploration = False
        print('init communication...')

    def first_communication(self):
        """
        communication to be held start of the exploration
        :return: void
        """
        self.connect()
        self.start_listen(self.expl)
        self.message_test_planet(self.expl, input('Planet Name: '))
        self.message_ready(self.expl)
        self.listen()
        self.stop_listen('explorer/013')
        self.disconnect()
    def node_comm_part_one(self):
        """
        communication to be held at each node part one
        :return: void
        """
        self.connect()
        self.start_listen('explorer/013')
        self.start_listen(self.planet_url(self.planetName))
        self.message_path()                         #send path taken (get from Planet Obj)
        self.listen()                               #handle results

    def node_comm_part_two(self, select):
        """
        communication to be held at each node part two
        :param select: Dict with next node {"Xs": _, "Ys": _, "Ds": _}
        :return: void
        """
        self.message_select(self.planet_url(self.planetName),
                            select['Xs'],
                            select['Ys'],
                            select['Ds'])
        self.listen()                                #handle results
        self.stop_listen('explorer/013')
        self.stop_listen(self.planet_url(self.planetName))
        self.disconnect()

    def message_handler(self, message):
        """
        handle response for on_message
        :param message: {"from": String , "type": String , ?"payload": Dict}
        :return: void
        """
        print('from {}:'.format(message["from"]))
        print('got payload: {}'.format(message.get("payload")) + ', with type: {}'.format(message["type"]))

        #sorry für den hässlichen code, match case wollte igwie nicht und hatte keine lust das zu fixen :P
        if message["from"] == "server":
            if message["type"] == "planet":
                self.planet.setPlanet(message["payload"]["planetName"],
                                      message["payload"]["startX"],
                                      message["payload"]["startY"],
                                      message["payload"]["startOrientation"])
            elif message["type"] == "done":
                print('done - ' + message["payload"]["message"])
                self.end_exploration = True
            elif message["type"] == "pathSelect":
                self.planet.pathSelect(message["payload"]["startDirection"])        #send to Robot!!!!!!!!!!!!!!!
            elif message["type"] == "path":
                self.planet.pathCorrection(message["payload"]["startX"],
                                           message["payload"]["startY"],
                                           message["payload"]["startDirection"],
                                           message["payload"]["endX"],
                                           message["payload"]["endY"],
                                           message["payload"]["endDirection"],
                                           message["payload"]["pathStatus"],
                                           message["payload"]["pathWeight"])
            elif message["type"] == "pathUnveiled":
                self.planet.pathUnveiled(message["payload"]["startX"],
                                         message["payload"]["startY"],
                                         message["payload"]["startDirection"],
                                         message["payload"]["endX"],
                                         message["payload"]["endY"],
                                         message["payload"]["endDirection"],
                                         message["payload"]["pathStatus"],
                                         message["payload"]["pathWeight"])
            elif message["type"] == "target":
                self.planet.addTarget(message["payload"]["targetX"],
                                      message["payload"]["targetY"])
            else:
                print("error while handling connection")

        elif message["from"] == "debug":
            #print(message['type'])
            if message['type'] == "adjust":
                self.planet.adjust(message["payload"]["startX"],
                                   message["payload"]["startY"],
                                   message["payload"]["startDirection"],
                                   message["payload"]["endX"],
                                   message["payload"]["endY"],
                                   message["payload"]["endDirection"])
            else:
                print('debug: {}'.format(message["payload"]))

    def message_exploration_completed(self, topic, message):
        """
        publish explorationCompleted msg with message to topic
        :param message: String
        :param topic: 'explorer/013' | planetURL(...)
        :return: void
        """
        msg = {"from": "client", "type": "explorationCompleted", "payload": {"message": message}}
        self.send_message(topic, msg)

    def message_select(self, topic, Xs, Ys, Ds):
        """
        publish pathSelect msg with start parameters to topic
        :param topic: 'explorer/013' | planetURL(...)
        :param Xs: Int
        :param Ys: Int
        :param Ds: Int
        :return: void
        """
        msg = {"from": "client", "type": "pathSelect", "payload": {"Xs": Xs, "Ys": Ys, "startDirection": Ds}}
        self.send_message(topic, msg)

    def message_path(self, topic, Xs, Ys, Ds, Xe, Ye, De, pathStatus):
        """
        publish path msg with start and end points to topic
        :param topic: 'explorer/013' | planetURL(...)
        :param Xs: Int
        :param Ys: Int
        :param Ds: Int
        :param Xe: Int
        :param Ye: Int
        :param De: Int
        :return: void
        """
        msg = {"from": "client", "type": "path", "payload": {"Xs": Xs, "Ys": Ys, "startDirection": Ds,
                                                             "endX": Xe, "endY": Ye, "endDirection": De,
                                                             "pathStatus": pathStatus}}
        self.send_message(topic, msg)

    def planet_url(self, planetName):
        """
        return planetURL based on planetName
        :param planetName: String
        :return: String
        """
        return "planet/{}/013".format(planetName)

    def message_target_reached(self, topic, message):
        """
        publish targetReached msg with message to topic
        :param topic: 'explorer/013' | planetURL(...)
        :param message: String
        :return: void
        """
        msg = {"from": "client", "type": "targetReached", "payload": {"message": message}}
        self.send_message(topic, msg)

    def message_ready(self, topic):
        """
        publish ready msg to topic
        :param topic: 'explorer/013' | planetURL(...)
        :return: void
        """
        msg = {"from": "client", "type": "ready", "payload": None}
        self.send_message(topic, msg)

    def message_test_planet(self, topic, planet_name):
        """
        publish testPlanet msg with planetName to topic and set internal planetName
        :param topic: 'explorer/013' | planetURL(...)
        :param planet_name: String
        :return: void
        """
        self.planetName = planet_name
        msg = {"from": "client", "type": "testPlanet", "payload": {"planetName": planet_name}}
        self.send_message(topic, msg)

    def connect(self):
        """
        connect client to broker
        :return: void
        """
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        print('connected to mothership.inf.tu ...')

    def disconnect(self):
        """
        disconnect client from broker
        :return: void
        """
        self.client.disconnect()
        print('disconnected from mothership.inf ...')

    def start_listen(self, topic):
        """
        start listening into a specific channel
        :param topic: String
        :return: void
        """
        print('start listening on topic: {}...'.format(topic))
        self.client.loop_start()
        self.client.subscribe(topic, qos=2)

    def stop_listen(self, topic):
        """
        stop listening into a specific channel
        :param topic: String
        :return: void
        """
        print('stop listening on topic: {}...'.format(topic))
        self.client.loop_stop()
        self.client.unsubscribe(topic)

    def listen(self):
        """
        listen loop
        :return: void
        """
        timeout = 0
        while True:
            user_input = None
            #user_input = input('Enter disconnect to close the connection...\n')
            time.sleep(3)
            timeout += 1
            if user_input == 'disconnect' or not self.received_msg:
                break
            self.received_msg = False
            if timeout > 10:
                print('listener timed out...')
                break

    # DO NOT EDIT THE METHOD SIGNATURE
    def on_message(self, client, data, message):
        """
        Handles the callback if any message arrived
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        payload = json.loads(message.payload.decode('utf-8'))
        self.logger.debug(json.dumps(payload, indent=2))
        # YOUR CODE FOLLOWS (remove pass, please!)
        #print('Got message with topic "{}":'.format(message.topic) + ' , data: {}'.format(data))
        self.received_msg = True
        self.message_handler(payload)

    # DO NOT EDIT THE METHOD SIGNATURE
    #
    # In order to keep the logging working you must provide a topic string and
    # an already encoded JSON-Object as message.
    def send_message(self, topic, message):
        """
        Sends given message to specified channel
        :param topic: String
        :param message: Object
        :return: void
        """
        self.logger.debug('Send to: ' + topic)
        self.logger.debug(json.dumps(message, indent=2))

        # YOUR CODE FOLLOWS (remove pass, please!)
        print('message to: ' + topic + ', message: ' + str(message))
        self.client.publish(topic, payload=self.create_msg(message), qos=2)

    def create_msg(self, message):
        msg = "{"
        msg = msg + '''"from":"{}", "type":"{}"'''.format(message[format("from")], message["type"])
        if message["payload"] is not None:
            msg = msg + ', "payload":{'
            for keys in message["payload"]:
                msg = msg + '''"{}": "{}"'''.format(keys, message["payload"][keys])
            msg = msg + "}"
        msg = msg + "}"
        return msg

    # DO NOT EDIT THE METHOD SIGNATURE OR BODY
    #
    # This helper method encapsulated the original "on_message" method and handles
    # exceptions thrown by threads spawned by "paho-mqtt"
    def safe_on_message_handler(self, client, data, message):
        """
        Handle exceptions thrown by the paho library
        :param client: paho.mqtt.client.Client
        :param data: Object
        :param message: Object
        :return: void
        """
        try:
            self.on_message(client, data, message)
        except:
            import traceback
            traceback.print_exc()
            print('error in on_message')
            raise
