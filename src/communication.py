#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import paho.mqtt.client as mqtt
import ssl
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
        self.planetName = None
        self.client = mqtt_client
        self.client.tls_set(tls_version=ssl.PROTOCOL_TLS)
        self.client.on_message = self.safe_on_message_handler
        # Add your client setup here
        self.client.username_pw_set('013', password='F8mVbzVCC4')
        self.logger = logger
        self.planet = Planet()
        self.expl = 'explorer/013'
        print('init communication...')

    def message_handler(self, message):
        """
        handle response for on_message
        :param message: String
        :return: void
        """
        #print('message: {}'.format(message))
        #print('from: {}'.format(message["from"]))

        #sorry für den hässlichen code, match case wollte igwie nicht und hatte keine lust das zu fixen :P
        if message["from"] == "server":
            print(message["type"])
            if message["type"] == "planet":
                self.planet.setPlanet(message["payload"]["planetName"],
                                      message["payload"]["startX"],
                                      message["payload"]["startY"],
                                      message["payload"]["startOrientation"])
            elif message["type"] == "done":
                print(message["payload"]["message"])
            elif message["type"] == "pathSelect":
                self.planet.pathSelect(message["payload"]["startDirection"])
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

    def explorationCompleted(self, message):
        """
        send explorationCompleted msg with message
        :param message: String
        :return: void
        """
        msg = {"from": "client", "type": "explorationCompleted", "payload": {"message": message}}
        self.send_message(self.expl, msg)

    def pathSelect(self, Xs, Ys, Ds):
        """
        send pathSelect msg with start parameters
        :param Xs: Int
        :param Ys: Int
        :param Ds: Int
        :return: void
        """
        msg = {"from": "client", "type": "pathSelect", "payload": {"Xs": Xs, "Ys": Ys, "startDirection": Ds}}
        self.send_message(self.planetURL(self.planetName), msg)

    def path(self, Xs, Ys, Ds, Xe, Ye, De, pathStatus):
        """
        send path msg with start and end points
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
        self.send_message(self.planetURL(self.planetName), msg)

    def planetURL(self, planetName):
        """
        return planetURL based on planetName
        :param planetName: String
        :return: String
        """
        return "planet/{}/013".format(planetName)

    def targetReached(self, message):
        """
        send targetReached msg with message
        :param message: String
        :return: void
        """
        msg = {"from": "client", "type": "targetReached", "payload": {"message": message}}
        self.send_message(self.expl, msg)

    def ready(self):
        """
        send ready msg
        :return: void
        """
        msg = {"from": "client", "type": "ready", "payload": None}
        self.send_message(self.expl, msg)

    def testPlanet(self, planetName):
        """
        send testPlanet msg with planetName and set planetName
        :param planetName: String
        :return: void
        """
        self.planetName = planetName
        msg = {"from": "client", "type": "testPlanet", "payload": {"planetName": planetName}}
        self.send_message(self.expl, msg)

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

    def listen(self, topic):
        """
        listen into a specific channel
        :param topic: String
        :return: void
        """
        self.client.loop_start()
        self.client.subscribe(topic, qos=2)
        while True:
            self.testPlanet("moin")
            user_input = input('Enter disconnect to close the connection...\n')
            if user_input == 'disconnect':
                break
        self.client.loop_stop()

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
