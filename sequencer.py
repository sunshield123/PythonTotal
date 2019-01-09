"""
Module has sequencer logic
"""

import json
import socket
import threading
from config import BROADCAST, PROCESSES


class Sequencer(threading.Thread):
    """
    Sequencer class, which sends sequence id for each message
    """

    def __init__(self, process_name, ip, port):
        """

        Args:
            process_name: process name
            ip: ip
            port: port
        """
        threading.Thread.__init__(self)

        self.shutdown_flag = threading.Event()
        self.process_name = process_name
        self.ip = ip
        self.port = port
        self.sock = None
        self.buffer_size = 1024

    def run(self):
        """
        It creates  sequence order and listens for incoming messages

        """
        print('Thread #%s started' % self.ident)

        # Create Socket which listens for messages
        self.sock = socket.socket(family=socket.AF_INET,
                                  type=socket.SOCK_DGRAM)

        self.sock.bind((self.ip, int(self.port)))
        print("Process name: {}".format(self.process_name))
        print("bound at")
        print((self.ip, int(self.port)))
        sequencer_id = 0

        message_sequence_data = {}
        while not self.shutdown_flag.is_set():

            # Get message data from processes

            data = self.sock.recvfrom(self.buffer_size)
            client_address = data[1]
            message = data[0]
            data = json.loads(message)

            message_sender = data["sender"]
            print("{} got message from {} and message is {}".format(self.process_name,
                                                                    message_sender,
                                                                    data["message"]))

            # check if message was set by one of the defined processes
            if message_sender in PROCESSES:

                # checks, if it has received duplicate message from same process
                key = (data["message"], data["sender"], client_address)
                if self.check_duplicate_message(message_sequence_data, key):
                    message_data = self.prepare_message(data,
                                                        message_sequence_data[key])
                    self.broadcast_message(message_data[0])
                    continue
                message_sequence_data[key] = sequencer_id
                message_data = self.prepare_message(data, sequencer_id)
                # broadcasts messages
                print("broad cast message")
                self.broadcast_message(message_data[0])
                sequencer_id = message_data[1] + 1

        # ... Clean shutdown code here ...
        print('Thread #%s stopped' % self.ident)

    def check_duplicate_message(self, message_sequence_data, key):
        """
        Checks if this message has been broadcast by same process or not
        Args:
            message_sequence_data: message sequence data dict
            key: dict key

        Returns:
            True or False
        """
        for dict_key in message_sequence_data.keys():
            if dict_key == key:
                return True

        return False

    def broadcast_message(self, bytes_to_send):
        """
        It broadcasts message to each process
        Args:
            bytes_to_send: bytes need to be send

        """

        for client in BROADCAST:
            print("broad cast message")
            if (self.ip, self.port) != client:
                self.sock.sendto(bytes_to_send, client)

    def prepare_message(self, data, sequence_id):
        """
        Prepare data which need to be send on
        network to other processes
        Args:
            data: data
            sequence_id: generated sequence id

        Returns:
            tuple of bytes need to be send and message id
        """
        print("message and its sequence number {}, {}".format(data["message"],sequence_id))
        data["message_id"] = sequence_id
        data["sequencer_sender"] = self.process_name
        bytes_to_send = str.encode(json.dumps(data))
        return bytes_to_send, sequence_id
