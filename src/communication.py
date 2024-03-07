#!/usr/bin/env python3

# Attention: Do not import the ev3dev.ev3 module in this file
import json
import paho.mqtt.client as mqtt
import ssl


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
        self.client.username_pw_set('013', password='F8mVbzVCC4')
        self.connect()
        self.logger = logger
        print('init communication...')

    def connect(self):
        self.client.connect('mothership.inf.tu-dresden.de', port=8883)
        print('connected to mothership.inf.tu ...')

    def disconnect(self):
        self.client.disconnect()
        print('disconnected from mothership.inf ...')

    def listen(self, topic):
        self.client.loop_start()
        self.client.subscribe(topic, qos=2)
        while True:
            user_input = input('Enter disconnect to close the connection...\n')
            if user_input == 'disconnect':
                break
            # add code here
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
        print('Got message with topic "{}":'.format(message.topic) + ' , data: {}'.format(data))

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
        out = {"from": "client", "type": "{}".format(message["type"])}
        if message["payload"] is not None:
            out["payload"] = message["payload"]
        self.client.publish(topic, json.dumps(out), qos=2)

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
            raise
