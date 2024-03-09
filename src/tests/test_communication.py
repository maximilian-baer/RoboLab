#!/usr/bin/env python3

import unittest.mock
import paho.mqtt.client as mqtt
import uuid

from communication import Communication

"""
IMPORTANT: THOSE TESTS ARE NOT REQUIRED FOR THE EXAM AND USED ONLY FOR DEVELOPMENT
ASK YOUR TUTOR FOR SPECIFIC DETAILS ABOUT THIS!
"""


class TestRoboLabCommunication(unittest.TestCase):
    @unittest.mock.patch('logging.Logger')
    def setUp(self, mock_logger):
        """
        Instantiates the communication class
        """
        client_id = '013-' + str(uuid.uuid4())  # Replace YOURGROUPID with your group ID
        client = mqtt.Client(client_id=client_id,  # Unique Client-ID to recognize our program
                             clean_session=False,  # We want to be remembered
                             protocol=mqtt.MQTTv311  # Define MQTT protocol version
                             )

        # Initialize your data structure here
        self.communication = Communication(client, mock_logger)
        self.syntaxTopic = 'comtest/013'

    def test_message_ready(self):
        """
        This test should check the syntax of the message type "ready"
        """
        try:
            self.communication.connect()
            self.communication.start_listen(self.syntaxTopic)
            self.communication.message_ready(self.syntaxTopic)
            self.communication.listen()
            self.communication.stop_listen(self.syntaxTopic)
            self.communication.disconnect()
        except:
            self.fail('error in message_ready')

    def test_message_path(self):
        """
        This test should check the syntax of the message type "path"
        """
        Xs = 0; Ys = 0; Ds = 0; Xe = 0; Ye = 0; De = 0; pathStatus = "free"
        try:
            self.communication.connect()
            self.communication.start_listen(self.syntaxTopic)
            self.communication.message_path(self.syntaxTopic, Xs, Ys, Ds, Xe, Ye, De, pathStatus)
            self.communication.listen()
            self.communication.stop_listen(self.syntaxTopic)
            self.communication.disconnect()
        except:
            self.fail('error in message_path')

    def test_message_path_invalid(self):
        """
        This test should check the syntax of the message type "path" with errors/invalid data
        """
        Xs = -1000; Ys = -1000; Ds = -1000; Xe = -1000; Ye = -1000; De = -1000; pathStatus = "rndm_word"
        try:
            self.communication.connect()
            self.communication.start_listen(self.syntaxTopic)
            self.communication.message_path(self.syntaxTopic, Xs, Ys, Ds, Xe, Ye, De, pathStatus)
            self.communication.listen()
            self.communication.stop_listen(self.syntaxTopic)
            self.communication.disconnect()
        except:
            self.fail('error with invalid message_path')


    def test_message_select(self):
        """
        This test should check the syntax of the message type "pathSelect"
        """
        Xs = 0; Ys = 0; Ds = 0
        try:
            self.communication.connect()
            self.communication.start_listen(self.syntaxTopic)
            self.communication.message_select(self.syntaxTopic, Xs, Ys, Ds)
            self.communication.listen()
            self.communication.stop_listen(self.syntaxTopic)
            self.communication.disconnect()
        except:
            self.fail('error in message_select')

    def test_message_complete(self):
        """
        This test should check the syntax of the message type "explorationCompleted" or "targetReached"
        """
        self.fail('implement me!')


if __name__ == "__main__":
    unittest.main()
